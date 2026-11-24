# Results summary

## Absolute grading (shift in P(correct) vs plain)

| side    | style          |   shift |   ci_lo |   ci_hi |   flip_rate |   n |
|:--------|:---------------|--------:|--------:|--------:|------------:|----:|
| correct | plain          |   0     |   0     |   0     |       0     |  29 |
| correct | reworded       |  -0.009 |  -0.041 |   0.016 |       0.034 |  29 |
| correct | formatted      |  -0.014 |  -0.026 |  -0.003 |       0     |  29 |
| correct | long           |  -0.035 |  -0.058 |  -0.013 |       0.043 |  23 |
| correct | short          |   0.036 |   0.009 |   0.068 |       0.034 |  29 |
| correct | confident      |  -0.106 |  -0.152 |  -0.066 |       0.115 |  26 |
| correct | technical      |  -0.009 |  -0.024 |   0.006 |       0.036 |  28 |
| correct | conversational |  -0.042 |  -0.074 |  -0.01  |       0.069 |  29 |
| wrong   | plain          |   0     |   0     |   0     |       0     |  30 |
| wrong   | reworded       |   0.011 |  -0.01  |   0.03  |       0.033 |  30 |
| wrong   | formatted      |   0.02  |   0.002 |   0.04  |       0     |  30 |
| wrong   | long           |   0.019 |  -0.001 |   0.04  |       0.045 |  22 |
| wrong   | short          |   0.023 |   0.001 |   0.045 |       0     |  30 |
| wrong   | confident      |  -0.044 |  -0.069 |  -0.022 |       0.037 |  27 |
| wrong   | technical      |   0.016 |  -0.002 |   0.035 |       0     |  29 |
| wrong   | conversational |  -0.001 |  -0.021 |   0.021 |       0     |  30 |


## Pairwise (accuracy, flips vs plain/plain)

| correct_style   | wrong_style    | order         |   accuracy |   baseline_accuracy |   ci_lo |   ci_hi |   flip_rate |   n |
|:----------------|:---------------|:--------------|-----------:|--------------------:|--------:|--------:|------------:|----:|
| plain           | plain          | correct_first |      0.897 |               0.897 |   0.793 |   1     |       0     |  29 |
| plain           | plain          | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| plain           | plain          | both          |      0.931 |               0.931 |   0.862 |   0.983 |       0     |  58 |
| reworded        | plain          | correct_first |      0.897 |               0.897 |   0.793 |   1     |       0     |  29 |
| reworded        | plain          | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| reworded        | plain          | both          |      0.931 |               0.931 |   0.862 |   0.983 |       0     |  58 |
| plain           | reworded       | correct_first |      0.931 |               0.897 |   0.828 |   1     |       0.034 |  29 |
| plain           | reworded       | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| plain           | reworded       | both          |      0.948 |               0.931 |   0.879 |   1     |       0.017 |  58 |
| formatted       | plain          | correct_first |      0.897 |               0.897 |   0.793 |   1     |       0     |  29 |
| formatted       | plain          | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| formatted       | plain          | both          |      0.931 |               0.931 |   0.862 |   0.983 |       0     |  58 |
| plain           | formatted      | correct_first |      0.897 |               0.897 |   0.793 |   1     |       0     |  29 |
| plain           | formatted      | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| plain           | formatted      | both          |      0.931 |               0.931 |   0.862 |   0.983 |       0     |  58 |
| long            | plain          | correct_first |      0.913 |               0.913 |   0.783 |   1     |       0     |  23 |
| long            | plain          | wrong_first   |      0.957 |               0.957 |   0.87  |   1     |       0     |  23 |
| long            | plain          | both          |      0.935 |               0.935 |   0.848 |   1     |       0     |  46 |
| plain           | long           | correct_first |      0.864 |               0.864 |   0.682 |   1     |       0     |  22 |
| plain           | long           | wrong_first   |      0.955 |               0.955 |   0.864 |   1     |       0     |  22 |
| plain           | long           | both          |      0.909 |               0.909 |   0.818 |   0.977 |       0     |  44 |
| short           | plain          | correct_first |      0.828 |               0.897 |   0.69  |   0.966 |       0.069 |  29 |
| short           | plain          | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| short           | plain          | both          |      0.897 |               0.931 |   0.81  |   0.966 |       0.034 |  58 |
| plain           | short          | correct_first |      0.862 |               0.897 |   0.724 |   0.966 |       0.034 |  29 |
| plain           | short          | wrong_first   |      0.931 |               0.966 |   0.828 |   1     |       0.034 |  29 |
| plain           | short          | both          |      0.897 |               0.931 |   0.81  |   0.966 |       0.034 |  58 |
| confident       | plain          | correct_first |      0.846 |               0.885 |   0.692 |   0.962 |       0.038 |  26 |
| confident       | plain          | wrong_first   |      0.885 |               0.962 |   0.769 |   1     |       0.077 |  26 |
| confident       | plain          | both          |      0.865 |               0.923 |   0.769 |   0.942 |       0.058 |  52 |
| plain           | confident      | correct_first |      0.923 |               0.885 |   0.808 |   1     |       0.038 |  26 |
| plain           | confident      | wrong_first   |      0.962 |               0.962 |   0.885 |   1     |       0     |  26 |
| plain           | confident      | both          |      0.942 |               0.923 |   0.865 |   1     |       0.019 |  52 |
| technical       | plain          | correct_first |      0.893 |               0.893 |   0.785 |   1     |       0     |  28 |
| technical       | plain          | wrong_first   |      0.964 |               0.964 |   0.893 |   1     |       0     |  28 |
| technical       | plain          | both          |      0.929 |               0.929 |   0.857 |   0.982 |       0     |  56 |
| plain           | technical      | correct_first |      0.857 |               0.893 |   0.714 |   0.964 |       0.036 |  28 |
| plain           | technical      | wrong_first   |      0.964 |               0.964 |   0.893 |   1     |       0     |  28 |
| plain           | technical      | both          |      0.911 |               0.929 |   0.821 |   0.982 |       0.018 |  56 |
| conversational  | plain          | correct_first |      0.862 |               0.897 |   0.724 |   0.966 |       0.034 |  29 |
| conversational  | plain          | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| conversational  | plain          | both          |      0.914 |               0.931 |   0.844 |   0.983 |       0.017 |  58 |
| plain           | conversational | correct_first |      0.897 |               0.897 |   0.793 |   1     |       0     |  29 |
| plain           | conversational | wrong_first   |      0.966 |               0.966 |   0.897 |   1     |       0     |  29 |
| plain           | conversational | both          |      0.931 |               0.931 |   0.862 |   0.983 |       0     |  58 |
