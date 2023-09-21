# Machine-Learning-for-Streaming-Data-with-Python
Machine Learning for Streaming Data with Python, published by Packt
### Specific Errors

#### `Code Block 2-6`:

- I add a cell above this block because there is no corresponding==`example.json`==, so in this added cell I write codes to create a `example.json`:

  ```python
  import json
  
  data = {"value": "hello"}
  
  with open("example.json", "w") as json_file:
      json.dump(data, json_file)
  ```

#### `Code Block 3-10 ~ 3-12`: 

- Fix the ==`indentation`== problem in the last row,  respectively.

#### `Code Block 5-1`:

- At the end of the last row, there is an extra equals sign ==`=`==.

#### `Code Block 5-9 & 5-14`: 

- There is no more a ==`QuantileThresholder`== method in the latest version of River, Instead, a ==`QuantileFilter`== method is appreciated.
- Reference: [River 0.11.0 Release Notes](https://riverml.xyz/dev/releases/0.11.0/)

#### `Code Block 5-10 ~ 5-13`:

- I believe that due to the change of `QuantileFilter` method, the domain of the original ==`scores`== list is not anymore boolean, but a float domain between [0, 1], thus i modify the codes as following:

  ```python
  # 5-10
  is_anomaly = []
  for datapoint in total_data:
      score = model.score_one({"x": datapoint})
      is_anomaly.append(model.classify(score))
      
  # 5-11
  import pandas as pd
  
  results = pd.DataFrame({"data": total_data, "is_anomaly": is_anomaly})
  results["actual_outlier"] = (results["data"] > 1) | (results["data"] < 0)
  
  # there are 20 actual outliers
  results["actual_outlier"].value_counts()
  
  # 5-12
  ## the algo detected 7 outliers
  results["is_anomaly"].value_counts()
  
  # 5-13
  ## in the 7 detected otuliuers, they're all actual outliers
  results.groupby("actual_outlier")["is_anomaly"].sum()
  ```

- Reference: [River API - QuantileFilter](https://riverml.xyz/dev/api/anomaly/QuantileFilter/)

- I do the same modify for the ==`HalfSpaceTrees`== part. 

#### `Code Block 6-12`:

- There is no more ==`AdaptiveRandomForestClassifier()`== method in `river.ensemble`, instead, There is a ==`ARFClassifier`== method in `river.forest`.
- Reference: [River ARI - ARFClassifier](https://riverml.xyz/dev/api/forest/ARFClassifier/)

#### `Code Block 8-3`:

- `states = set(rounded_values)` raises an error ==`ValueError: index cannot be a set`==, use `states = list(rounded_values)` would fix this.

#### `Code Block 8-4 ~ 8-6`:

- If I understand correctly, you want to process data individually, but using the `pandas.DataFrame.loc` method with code like ==`policy.loc[current_value, :]`== will work with rows of data rather than individual values. This is because the values have been rounded, so if there are 300 occurrences of `-0.9` in `rounded_values`, `policy.loc[current_value, :]` will also return 300 rows.

- Therefore, I have switched to using the `pandas.DataFrame.iloc` method, which allows me to access specific rows using integer-based indexing within this paradigm.

  ```python
  # 8-4
  def find_action(policy, current_state):
      if policy.iloc[current_state, :].sum() == 0:
          return random.choice(["buy", "sell"])
  
      return policy.columns[policy.iloc[current_state, :].argmax()]
      
  # 8-5
  Action = dict({"buy": 0, "sell": 1})
  
  
  def update_policy(reward, current_state, action):
      LEARNING_RATE = 0.1
      MAX_REWARD = 10
      DISCOUNT_FACTOR = 0.05
  
      return LEARNING_RATE * (
          reward
          + DISCOUNT_FACTOR * MAX_REWARD
          - policy.iloc[current_state, Action[action]]
      )
    
  # 8-6  
  past_state_value = 0
  past_action = "buy"
  total_reward = 0.0
  rewards = []
  
  for i, current_state_value in enumerate(rounded_values):
      # do the action
      action = find_action(policy, i)
  
      # also compute reward from previous action and update state
      if past_action == "buy":
          reward = current_state_value - past_state_value
  
      if past_action == "sell":
          reward = past_state_value - current_state_value
  
      total_reward = total_reward + float(reward)
  
      policy.iloc[i, Action[action]] += update_policy(reward, i, action)
  
      # print(policy)
      rewards.append(total_reward)
  
      past_action = action
      past_state_value = current_state_value
  ```

#### `Code Block 11-1`:

- The =='+'== operator in this block would raise an error: `SyntaxError: invalid syntax`, thus I modify this block to:

  ```python
  import random
  
  X = [i // 3 + 1 for i in range(30)]
  y = [x + random.random() for x in X[:15]] + [x * 2 + random.random() for x in X[15:]]
  ```

#### `Code Block 11-4 & 11-5 & 11-8`:

- There isn't a ==`window_size`== method in `KNNRegressor`, instead, `n_neighbors` is appreciated.

#### Besides

I've formatted these .ipynb files using following codes in terminal:

1. Install the required packages:

   ```
   pip install -U nbqa black isort pyupgrade
   ```

2. Navigate to the folder containing the `.ipynb` files:

   ```
   cd <folder_path>
   ```

3. Format the files using `black`:

   ```
   nbqa black *.ipynb
   ```

4. Sort the imports using `isort`:

   ```
   nbqa isort *.ipynb
   ```

5. Upgrade the code to modern Python using `pyupgrade`:

   ```
   nbqa pyupgrade *.ipynb
   ```

These commands will help ensure consistent formatting and apply necessary upgrades to Jupyter Notebook files.

Once again, thank you very much for composing this book and chscking my issues.

😗
