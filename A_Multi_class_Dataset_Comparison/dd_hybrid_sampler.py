
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np
from numpy.typing import ArrayLike
from sklearn.base import BaseEstimator
from sklearn.neighbors import NearestNeighbors
from sklearn.utils.validation import check_X_y

@dataclass
class DDHybridSampler(BaseEstimator):
    k: int = 5
    k_smote: int = 5
    border_share: float = 0.75
    target_ir: float = 1.5
    q_start: float = 0.60
    q_step: float = 0.05
    max_us_iters: int = 6
    per_iter_us_cap: Optional[float] = 0.30
    random_state: Optional[int] = None

    def fit_resample(self, X: ArrayLike, y: ArrayLike) -> Tuple[np.ndarray, np.ndarray]:
        X, y = check_X_y(X, y)
        rng = np.random.default_rng(self.random_state)
        y = y.astype(int)
        classes = np.unique(y)
        if classes.size != 2:
            raise ValueError("This draft supports binary classification only (labels in {0,1}).")

        # Identify majority/minority (labels unchanged)
        c0, c1 = classes
        n0, n1 = (y == c0).sum(), (y == c1).sum()
        maj_label, min_label = (c0, c1) if n0 > n1 else (c1, c0)

        Xw = X.copy()
        yw = y.copy()

        ir = self._imbalance_ratio(yw, maj_label, min_label)
        if ir <= self.target_ir:
            return Xw, yw

        Xw, yw = self._oversample_knn(Xw, yw, maj_label, min_label, rng)
        Xw, yw = self._iterative_prune(Xw, yw, maj_label, min_label, rng)
        return Xw, yw

    @staticmethod
    def _imbalance_ratio(y: np.ndarray, maj_label: int, min_label: int) -> float:
        nM = np.sum(y == maj_label)
        nm = np.sum(y == min_label)
        return (nM / max(nm, 1))

    def _neighbors(self, X: np.ndarray, k: int):
        k_eff = min(k + 1, len(X))
        nn = NearestNeighbors(n_neighbors=k_eff)
        nn.fit(X)
        d, idx = nn.kneighbors(X)
        return d[:, 1:], idx[:, 1:]

    def _minority_categories(self, X: np.ndarray, y: np.ndarray, min_label: int):
        d, idx = self._neighbors(X, self.k)
        y_n = y[idx]
        opp_counts = (y_n != y[:, None]).sum(axis=1)

        minority_mask = (y == min_label)
        opp_m = opp_counts[minority_mask]
        safe_m = opp_m <= 1
        border_m = (opp_m >= 2) & (opp_m <= 3)
        outlier_m = opp_m >= 4
        return minority_mask, safe_m, border_m, outlier_m, (d, idx)

    def _oversample_knn(self, X: np.ndarray, y: np.ndarray, maj_label: int, min_label: int, rng):
        nM = np.sum(y == maj_label)
        nm = np.sum(y == min_label)
        ir = nM / max(nm, 1)
        if ir <= self.target_ir:
            return X, y

        target_minority = int(np.ceil(nM / self.target_ir))
        n_synth = max(0, target_minority - nm)
        if n_synth == 0:
            return X, y

        minority_mask, safe_m, border_m, outlier_m, (d, idx) = self._minority_categories(X, y, min_label)
        min_idx_all = np.where(minority_mask)[0]
        safe_idx = min_idx_all[safe_m]
        border_idx = min_idx_all[border_m]

        n_border = len(border_idx)
        n_safe = len(safe_idx)
        if (n_border + n_safe) == 0:
            return X, y

        n_border_goal = int(round(self.border_share * n_synth))
        n_safe_goal = n_synth - n_border_goal
        if n_border == 0:
            n_safe_goal = n_synth
            n_border_goal = 0
        elif n_safe == 0:
            n_border_goal = n_synth
            n_safe_goal = 0

        X_syn, y_syn = [], []

        def synth_from(seeds: np.ndarray, n_needed: int):
            if n_needed <= 0 or seeds.size == 0:
                return
            min_mask = (y == min_label)
            X_min = X[min_mask]
            k_eff = min(self.k_smote + 1, len(X_min))
            nn = NearestNeighbors(n_neighbors=k_eff)
            nn.fit(X_min)
            d_m, idx_m = nn.kneighbors(X_min)

            min_global_idx = np.where(min_mask)[0]
            global_to_local = {g: i for i, g in enumerate(min_global_idx)}

            for _ in range(n_needed):
                s = rng.choice(seeds)
                s_local = global_to_local.get(s)
                if s_local is None:
                    continue
                neigh_locals = idx_m[s_local, 1:]
                if neigh_locals.size == 0:
                    x1 = X[s]; x2 = x1
                else:
                    j_local = rng.choice(neigh_locals)
                    x1 = X[s]
                    x2 = X[min_global_idx[j_local]]
                lam = rng.random()
                x_new = x1 + lam * (x2 - x1)
                X_syn.append(x_new)
                y_syn.append(min_label)

        def distribute(n_goal: int, seeds: np.ndarray):
            if n_goal <= 0 or seeds.size == 0:
                return 0, np.array([], dtype=int)
            base = n_goal // len(seeds)
            rem = n_goal % len(seeds)
            counts = np.full(len(seeds), base, dtype=int)
            if rem > 0:
                extra_idx = np.random.default_rng(self.random_state).choice(len(seeds), size=rem, replace=False)
                counts[extra_idx] += 1
            expanded = np.repeat(seeds, counts)
            return expanded.size, expanded

        n_border_alloc, border_expanded = distribute(n_border_goal, border_idx)
        n_safe_alloc, safe_expanded = distribute(n_safe_goal, safe_idx)
        synth_from(border_expanded, n_border_alloc)
        synth_from(safe_expanded, n_safe_alloc)

        if X_syn:
            X_new = np.vstack([X, np.vstack(X_syn)])
            y_new = np.concatenate([y, np.array(y_syn, dtype=y.dtype)])
            return X_new, y_new
        else:
            return X, y

    def _iterative_prune(self, X: np.ndarray, y: np.ndarray, maj_label: int, min_label: int, rng):
        qd = float(self.q_start)
        Xw, yw = X, y

        for _ in range(self.max_us_iters):
            ir = self._imbalance_ratio(yw, maj_label, min_label)
            if ir <= self.target_ir:
                break
            d, idx = self._neighbors(Xw, self.k)
            y_n = yw[idx]

            G_mask = (yw == maj_label)
            M_mask = (yw == min_label)
            if not np.any(G_mask) or not np.any(M_mask):
                break

            opp_counts = (y_n != yw[:, None]).sum(axis=1)
            u = opp_counts[G_mask]

            from sklearn.metrics import pairwise_distances
            d_to_min = pairwise_distances(Xw[G_mask], Xw[M_mask], metric="euclidean")
            dmin = d_to_min.min(axis=1)

            rk_all = d[:, -1]
            rk = rk_all[G_mask]
            density = 1.0 / (rk + 1e-12)

            if len(dmin) < 2 or len(density) < 2:
                break
            dmin_thr = np.quantile(dmin, qd)
            dens_thr = np.quantile(density, 1 - qd)

            elig = (u <= 1) & (dmin >= dmin_thr) & (density >= dens_thr)
            if not np.any(elig):
                qd = max(0.0, qd - self.q_step)
                continue

            elig_idx_global = np.where(G_mask)[0][elig]

            if self.per_iter_us_cap is not None:
                nG = G_mask.sum()
                cap = int(np.floor(self.per_iter_us_cap * nG))
                if cap > 0 and elig_idx_global.size > cap:
                    order = np.lexsort((-dmin[elig], -density[elig]))
                    elig_idx_global = elig_idx_global[order[:cap]]

            keep_mask = np.ones(len(yw), dtype=bool)
            keep_mask[elig_idx_global] = False
            Xw = Xw[keep_mask]
            yw = yw[keep_mask]

            if self._imbalance_ratio(yw, maj_label, min_label) > self.target_ir:
                qd = max(0.0, qd - self.q_step)

        return Xw, yw
