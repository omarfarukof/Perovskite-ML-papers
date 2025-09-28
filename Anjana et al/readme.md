ABX₃ Perovskite ML Dataset
    Dataset Genesis
      OQMD 1M+ DFT entries
      16 323 ABX₃ structures
      Exclude anti-perovskites
      Hull filter ≤ 5 eV/atom
    Feature Engineering
      61 total inputs
      55 physicochemical
        mean & std per site
      2 stability
        Goldschmidt gtf
        Octahedral factor of
      4 OQMD
        vol, Es, Ef, Eg
    Targets
      Formation Energy Ef
      Band Gap Eg
      Crystal System cs
    ML Pipeline
      Pre-processing
        Impute median
        Standard scale
      Train/Test 70:30
      Algorithms
        SVR
        Random Forest
        XGBoost
        LightGBM
    Experiments
      Regression
        Ef → best SVM 0.013 eV/atom
        Eg → best LGB 0.216 eV
      Classification
        4-class cs
        Down-sample 2 089 each
        Macro-F1 0.85
      Sampling Study
        Down-sample vs SMOTE
        SMOTE: cubic ↑, tetragonal ↓
    Evaluation
      MAE, RMSE, R²
      Accuracy, Precision, Recall, F1
      5-fold CV & Stratified CV
    Reproducibility
      Open dataset & code
      Fixed random seeds
      Saved pipelines
