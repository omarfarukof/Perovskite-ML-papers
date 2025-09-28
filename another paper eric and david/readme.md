# ABX₃ ML Benchmark Paper

    1.Motivation
      ABX₃ multifunctional
      Need fast surrogate models
    2.KnowledgeGap
      Small/oxide-only datasets
    3.Dataset
      OQMD 1M+ → 16k
      Anti-perovskite removed
      Energy above hull ≤5
    4.Features(61)
      Physico-chemical(55)
      Stability/Geometric(3)
      OQMD auxiliary
    5.Targets
      Regression: Ef, Eg
      Classification: Crystal-system
    6.ML-Pipeline
      Train/Test 70/30
      SVR/SVC
      RFR/RFC
      XGB
      LGB
      Down-sample / SMOTE
      Metrics: MAE RMSE R² F1
    7.Results
      Ef MAE 0.013 eV/atom (SVM)
      Eg MAE 0.216 eV (LGB)
      F1 0.85 (clf)
    8.Insights
      Es helps Ef
      DFT underestimates Eg
      Cubic-Tetragonal confusion
    9.Reproducibility
      Open CSV & code
    10.Future
      Deep generative
      Quantum descriptors
      Active learning
