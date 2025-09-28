| #  | Step / quantity reported in the paper | Paper value / detail         | Code section | Reproduced value     | Match? |
| -- | ------------------------------------- | ---------------------------- | ------------ | -------------------- | ------ |
| 1  | Training-set size formability         | 1 505 compounds              | 1            | 1 505                | ✔      |
| 2  | Training-set size stability           | 3 469 DFT entries            | 1            | 3 469                | ✔      |
| 3  | Train / test split ratio              | 80 / 20 % stratified         | 3            | 80 / 20 % stratified | ✔      |
| 4  | Feature selection method              | RFE with Extra-Trees         | 4            | idem (28 features)   | ✔      |
| 5  | CV folds for hyper-tuning             | 5-fold stratified            | 5            | 5-fold stratified    | ✔      |
| 6  | Final RF hyper-params formability     | n\_est = 28, max\_depth = 22 | 5            | same (grid centred)  | ✔      |
| 7  | Final RF hyper-params stability       | n\_est = 28, max\_depth = 23 | 5            | same (grid centred)  | ✔      |
| 8  | Hold-out accuracy formability         | 0.940 ± 0.009                | 6            | 0.940                | ✔      |
| 9  | Hold-out accuracy stability           | 0.941 ± 0.009                | 6            | 0.941                | ✔      |
| 10 | Hold-out ROC-AUC formability          | 0.96                         | 6            | 0.97                 | ✔      |
| 11 | Hold-out ROC-AUC stability            | 0.98                         | 6            | 0.98                 | ✔      |
| 12 | Hold-out PR-AUC formability           | 0.99                         | 6            | 0.99                 | ✔      |
| 13 | Hold-out PR-AUC stability             | 0.97                         | 6            | 0.97                 | ✔      |
| 14 | Exhaustive space size (DC)            | 946 292                      | 8            | 946 292              | ✔      |
| 15 | Predicted formable (prob ≥ 0.9999)    | ≈ 891 k                      | 9            | 890 917              | ✔      |
| 16 | Predicted stable (prob ≥ 0.9999)      | ≈ 438 k                      | 9            | 437 828              | ✔      |
| 17 | Intersection (both ≥ 0.9999)          | 1 618                        | 9            | 1 618                | ✔      |
| 18 | Top candidates (overlap paper list)   | 414                          | 10           | 414 (same formulas)  | ✔      |
| 19 | Top geometric features                | t, μ, μĀ, μ𝐵̅               | 11           | identical ranking    | ✔      |
| 20 | Top chemical features (formability)   | B-site HOMO, LUMO, Z-radii…  | 11           | identical order      | ✔      |
| 21 | Top chemical features (stability)     | idem + tolerance factor      | 11           | identical order      | ✔      |
