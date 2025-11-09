# Step 3 — XGBoost Modeling (Pseudohuber + Fine Weighting)

This notebook (`19-XGBoost-pseudohuber-fineweighting.ipynb`) presents the **final modeling phase** of the **ML Indy Housing** project, based on datasets that have already been standardized and normalized.

## Input Data

- **Input files:**
  `X_train_scaled-v2.csv`, `y_train-v2.csv`,
  `X_val_scaled-v2.csv`, `y_val-v2.csv`,
  `X_test_scaled-v2.csv`, `y_test-v2.csv`

These files already contain scaled data from the previous step (scaler files are not reused here).

### Number of Rows per Split
| Split | Number of Rows |
|:------------------------|-----------------:|
| `X_train_scaled-v2.csv` | 3,957 |
| `X_val_scaled-v2.csv`   | 849 |
| `X_test_scaled-v2.csv`  | 847 |

---

## 1. Preprocessing

- Loading of training, validation, and test splits.  
- No additional transformations were applied since standard and min-max scalers had already been used.  
- Implementation of a **fine weighting system** to balance the influence of houses according to their price.

### Weighting Formula

Each sample was assigned a weight:
\[
w_i = 1 + 2 \times \left( \frac{y_i}{\text{mean}(y)} \right)
\]
This approach moderately increases the weight of expensive homes without distorting the overall loss function.

The target variable used is the **natural logarithm of the sale price**:
\[
y = \log(\text{sale\_price})
\]
This transformation reduces skewness, stabilizes variance, and limits the influence of extreme values.

---

## 2. Model Choice

- **Algorithm:** `XGBRegressor`
- **Loss function:** `reg:pseudohubererror`, robust to outliers.
- **Main hyperparameters:**
  - `max_depth = 7`
  - `learning_rate = 0.03`
  - `colsample_bytree = 0.6`
  - `n_estimators = 1000`
  - `tree_method = 'gpu_hist'`, `predictor = 'gpu_predictor'`
- **Dynamic weighting** (`sample_weight`) applied during training to balance price ranges.

---

## 3. Cross-Validation

- **Method:** stratified 5-fold cross-validation.  
- **Average results:**
  - RMSE (log) = 0.254 ± 0.003  
  - Global MAE = **$68,781 ± 8,451**  
  - MAE for houses < $1M = **$48,709 ± 671**  
  - MAE for houses ≥ $1M = **$772,132 ± 356,900**

---

## 4. Test Set Evaluation

**Final results:**
- **Global MAE:** $56,085  
- **Standard houses (< $1M):** $45,195  
- **Luxury houses (≥ $1M):** $531,241  

**Corresponding relative errors:**
- **All houses:** 14.5 %  
- **Standard houses (< $1M):** 12.8 %  
- **Luxury houses (≥ $1M):** 29.6 %

---

## 5. Interpretation

The **XGBoost model with Pseudohuber loss and fine weighting** achieves a **very good balance between robustness and accuracy**:
- It predicts **standard homes** (about 98% of the market) with an average error below 13%.  
- **Luxury homes**, rarer and more variable, show larger deviations but remain stably modeled.

This model represents the **final reference** for the **ML Indy Housing** pipeline, combining statistical rigor, adaptive weighting, and robustness to outliers.
