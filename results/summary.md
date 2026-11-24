# Results summary

## Absolute grading (shift in P(correct) vs plain)

| side    | style          |   shift |   ci_lo |   ci_hi |   flip_rate |   n |
|:--------|:---------------|--------:|--------:|--------:|------------:|----:|
| correct | plain          |   0     |   0     |   0     |       0     |  80 |
| correct | reworded       |   0     |  -0.016 |   0.016 |       0.075 |  80 |
| correct | formatted      |   0.007 |  -0.002 |   0.016 |       0.025 |  80 |
| correct | long           |  -0.038 |  -0.053 |  -0.023 |       0.062 |  64 |
| correct | short          |   0.015 |   0.002 |   0.028 |       0.012 |  80 |
| correct | confident      |  -0.072 |  -0.092 |  -0.054 |       0.147 |  75 |
| correct | technical      |  -0     |  -0.015 |   0.016 |       0.065 |  77 |
| correct | conversational |  -0.008 |  -0.02  |   0.004 |       0.051 |  79 |
| wrong   | plain          |   0     |   0     |   0     |       0     |  80 |
| wrong   | reworded       |   0.002 |  -0.01  |   0.014 |       0     |  77 |
| wrong   | formatted      |  -0.003 |  -0.012 |   0.006 |       0.013 |  79 |
| wrong   | short          |   0.001 |  -0.007 |   0.009 |       0     |  73 |
| wrong   | confident      |  -0.04  |  -0.062 |  -0.021 |       0.045 |  67 |
| wrong   | technical      |   0.003 |  -0.008 |   0.012 |       0.014 |  74 |
| wrong   | conversational |   0.002 |  -0.01  |   0.018 |       0.012 |  80 |
| wrong   | long           |  -0.012 |  -0.029 |   0.004 |       0.031 |  64 |


## Pairwise (accuracy, flips vs plain/plain)

| correct_style   | wrong_style    | order         |   accuracy |   ci_lo |   ci_hi |   flip_rate |   n |
|:----------------|:---------------|:--------------|-----------:|--------:|--------:|------------:|----:|
| plain           | plain          | correct_first |      0.925 |   0.862 |   0.975 |       0     |  80 |
| plain           | plain          | wrong_first   |      0.962 |   0.912 |   1     |       0     |  80 |
| plain           | plain          | both          |      0.944 |   0.906 |   0.975 |       0     | 160 |
| reworded        | plain          | correct_first |      0.95  |   0.9   |   0.988 |       0.025 |  80 |
| reworded        | plain          | wrong_first   |      0.95  |   0.9   |   0.988 |       0.012 |  80 |
| reworded        | plain          | both          |      0.95  |   0.912 |   0.981 |       0.019 | 160 |
| plain           | reworded       | correct_first |      0.948 |   0.896 |   0.987 |       0.026 |  77 |
| plain           | reworded       | wrong_first   |      0.948 |   0.896 |   0.987 |       0.013 |  77 |
| plain           | reworded       | both          |      0.948 |   0.909 |   0.981 |       0.019 | 154 |
| formatted       | plain          | correct_first |      0.938 |   0.875 |   0.988 |       0.038 |  80 |
| formatted       | plain          | wrong_first   |      0.938 |   0.875 |   0.988 |       0.025 |  80 |
| formatted       | plain          | both          |      0.938 |   0.9   |   0.969 |       0.031 | 160 |
| plain           | formatted      | correct_first |      0.937 |   0.873 |   0.987 |       0.013 |  79 |
| plain           | formatted      | wrong_first   |      0.962 |   0.911 |   1     |       0     |  79 |
| plain           | formatted      | both          |      0.949 |   0.911 |   0.981 |       0.006 | 158 |
| long            | plain          | correct_first |      0.938 |   0.875 |   0.984 |       0.031 |  64 |
| long            | plain          | wrong_first   |      0.938 |   0.875 |   0.984 |       0.016 |  64 |
| long            | plain          | both          |      0.938 |   0.891 |   0.977 |       0.023 | 128 |
| short           | plain          | correct_first |      0.95  |   0.9   |   0.988 |       0.025 |  80 |
| short           | plain          | wrong_first   |      0.962 |   0.912 |   1     |       0     |  80 |
| short           | plain          | both          |      0.956 |   0.925 |   0.981 |       0.012 | 160 |
| plain           | short          | correct_first |      0.932 |   0.876 |   0.986 |       0.014 |  73 |
| plain           | short          | wrong_first   |      0.959 |   0.904 |   1     |       0.027 |  73 |
| plain           | short          | both          |      0.945 |   0.904 |   0.979 |       0.021 | 146 |
| confident       | plain          | correct_first |      0.907 |   0.84  |   0.96  |       0.013 |  75 |
| confident       | plain          | wrong_first   |      0.933 |   0.88  |   0.987 |       0.027 |  75 |
| confident       | plain          | both          |      0.92  |   0.873 |   0.96  |       0.02  | 150 |
| plain           | confident      | correct_first |      0.955 |   0.896 |   1     |       0.045 |  67 |
| plain           | confident      | wrong_first   |      0.97  |   0.925 |   1     |       0.015 |  67 |
| plain           | confident      | both          |      0.963 |   0.925 |   0.993 |       0.03  | 134 |
| technical       | plain          | correct_first |      0.935 |   0.87  |   0.987 |       0.013 |  77 |
| technical       | plain          | wrong_first   |      0.974 |   0.935 |   1     |       0.013 |  77 |
| technical       | plain          | both          |      0.955 |   0.922 |   0.987 |       0.013 | 154 |
| plain           | technical      | correct_first |      0.919 |   0.851 |   0.973 |       0.027 |  74 |
| plain           | technical      | wrong_first   |      0.946 |   0.892 |   0.986 |       0.014 |  74 |
| plain           | technical      | both          |      0.932 |   0.885 |   0.966 |       0.02  | 148 |
| conversational  | plain          | correct_first |      0.924 |   0.861 |   0.975 |       0.025 |  79 |
| conversational  | plain          | wrong_first   |      0.924 |   0.861 |   0.975 |       0.038 |  79 |
| conversational  | plain          | both          |      0.924 |   0.88  |   0.962 |       0.032 | 158 |
| plain           | conversational | correct_first |      0.925 |   0.862 |   0.975 |       0     |  80 |
| plain           | conversational | wrong_first   |      0.975 |   0.938 |   1     |       0.012 |  80 |
| plain           | conversational | both          |      0.95  |   0.912 |   0.981 |       0.006 | 160 |
| plain           | long           | correct_first |      0.938 |   0.875 |   0.984 |       0.031 |  64 |
| plain           | long           | wrong_first   |      0.969 |   0.922 |   1     |       0     |  64 |
| plain           | long           | both          |      0.953 |   0.914 |   0.984 |       0.016 | 128 |
