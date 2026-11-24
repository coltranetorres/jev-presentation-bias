# Results summary

## Absolute grading (shift in P(correct) vs plain)

| side    | style          |   shift |   ci_lo |   ci_hi |   flip_rate |   n |
|:--------|:---------------|--------:|--------:|--------:|------------:|----:|
| correct | plain          |   0     |   0     |   0     |       0     |  79 |
| correct | reworded       |  -0.001 |  -0.017 |   0.015 |       0.076 |  79 |
| correct | formatted      |   0.006 |  -0.002 |   0.015 |       0.025 |  79 |
| correct | long           |  -0.039 |  -0.053 |  -0.023 |       0.063 |  63 |
| correct | short          |   0.013 |   0.001 |   0.024 |       0.013 |  79 |
| correct | confident      |  -0.073 |  -0.092 |  -0.055 |       0.149 |  74 |
| correct | technical      |   0.003 |  -0.012 |   0.018 |       0.053 |  76 |
| correct | conversational |  -0.007 |  -0.018 |   0.005 |       0.051 |  78 |
| wrong   | plain          |   0     |   0     |   0     |       0     |  73 |
| wrong   | reworded       |   0.003 |  -0.009 |   0.016 |       0     |  70 |
| wrong   | formatted      |  -0.001 |  -0.01  |   0.009 |       0.014 |  72 |
| wrong   | short          |   0.002 |  -0.006 |   0.01  |       0     |  67 |
| wrong   | confident      |  -0.041 |  -0.066 |  -0.023 |       0.049 |  61 |
| wrong   | technical      |   0.002 |  -0.011 |   0.013 |       0.015 |  67 |
| wrong   | conversational |   0.004 |  -0.009 |   0.022 |       0.014 |  73 |
| wrong   | long           |  -0.01  |  -0.028 |   0.006 |       0.034 |  58 |


## Pairwise (accuracy, flips vs plain/plain)

| correct_style   | wrong_style    | order         |   accuracy |   baseline_accuracy |   ci_lo |   ci_hi |   flip_rate |   n |
|:----------------|:---------------|:--------------|-----------:|--------------------:|--------:|--------:|------------:|----:|
| plain           | plain          | correct_first |      0.958 |               0.958 |   0.903 |   1     |       0     |  72 |
| plain           | plain          | wrong_first   |      0.972 |               0.972 |   0.931 |   1     |       0     |  72 |
| plain           | plain          | both          |      0.965 |               0.965 |   0.938 |   0.993 |       0     | 144 |
| reworded        | plain          | correct_first |      0.972 |               0.958 |   0.931 |   1     |       0.014 |  72 |
| reworded        | plain          | wrong_first   |      0.972 |               0.972 |   0.931 |   1     |       0     |  72 |
| reworded        | plain          | both          |      0.972 |               0.965 |   0.944 |   0.993 |       0.007 | 144 |
| plain           | reworded       | correct_first |      0.971 |               0.957 |   0.928 |   1     |       0.014 |  69 |
| plain           | reworded       | wrong_first   |      0.957 |               0.971 |   0.899 |   1     |       0.014 |  69 |
| plain           | reworded       | both          |      0.964 |               0.964 |   0.928 |   0.993 |       0.014 | 138 |
| formatted       | plain          | correct_first |      0.958 |               0.958 |   0.903 |   1     |       0.028 |  72 |
| formatted       | plain          | wrong_first   |      0.972 |               0.972 |   0.931 |   1     |       0     |  72 |
| formatted       | plain          | both          |      0.965 |               0.965 |   0.931 |   0.993 |       0.014 | 144 |
| plain           | formatted      | correct_first |      0.958 |               0.958 |   0.901 |   1     |       0     |  71 |
| plain           | formatted      | wrong_first   |      0.972 |               0.972 |   0.93  |   1     |       0     |  71 |
| plain           | formatted      | both          |      0.965 |               0.965 |   0.93  |   0.993 |       0     | 142 |
| long            | plain          | correct_first |      0.964 |               0.946 |   0.911 |   1     |       0.018 |  56 |
| long            | plain          | wrong_first   |      0.964 |               0.964 |   0.911 |   1     |       0     |  56 |
| long            | plain          | both          |      0.964 |               0.955 |   0.929 |   0.991 |       0.009 | 112 |
| short           | plain          | correct_first |      0.972 |               0.958 |   0.931 |   1     |       0.014 |  72 |
| short           | plain          | wrong_first   |      0.972 |               0.972 |   0.931 |   1     |       0     |  72 |
| short           | plain          | both          |      0.972 |               0.965 |   0.944 |   0.993 |       0.007 | 144 |
| plain           | short          | correct_first |      0.955 |               0.955 |   0.894 |   1     |       0     |  66 |
| plain           | short          | wrong_first   |      0.985 |               0.97  |   0.955 |   1     |       0.015 |  66 |
| plain           | short          | both          |      0.97  |               0.962 |   0.939 |   0.992 |       0.008 | 132 |
| confident       | plain          | correct_first |      0.94  |               0.955 |   0.881 |   0.985 |       0.015 |  67 |
| confident       | plain          | wrong_first   |      0.97  |               0.97  |   0.925 |   1     |       0     |  67 |
| confident       | plain          | both          |      0.955 |               0.963 |   0.918 |   0.985 |       0.007 | 134 |
| plain           | confident      | correct_first |      0.983 |               0.95  |   0.95  |   1     |       0.033 |  60 |
| plain           | confident      | wrong_first   |      0.983 |               0.967 |   0.95  |   1     |       0.017 |  60 |
| plain           | confident      | both          |      0.983 |               0.958 |   0.958 |   1     |       0.025 | 120 |
| technical       | plain          | correct_first |      0.957 |               0.957 |   0.899 |   1     |       0     |  69 |
| technical       | plain          | wrong_first   |      0.986 |               0.971 |   0.957 |   1     |       0.014 |  69 |
| technical       | plain          | both          |      0.971 |               0.964 |   0.942 |   0.993 |       0.007 | 138 |
| plain           | technical      | correct_first |      0.955 |               0.955 |   0.894 |   1     |       0.03  |  66 |
| plain           | technical      | wrong_first   |      0.97  |               0.97  |   0.924 |   1     |       0     |  66 |
| plain           | technical      | both          |      0.962 |               0.962 |   0.924 |   0.992 |       0.015 | 132 |
| conversational  | plain          | correct_first |      0.958 |               0.958 |   0.901 |   1     |       0     |  71 |
| conversational  | plain          | wrong_first   |      0.958 |               0.972 |   0.901 |   1     |       0.014 |  71 |
| conversational  | plain          | both          |      0.958 |               0.965 |   0.923 |   0.986 |       0.007 | 142 |
| plain           | conversational | correct_first |      0.958 |               0.958 |   0.903 |   1     |       0     |  72 |
| plain           | conversational | wrong_first   |      0.986 |               0.972 |   0.958 |   1     |       0.014 |  72 |
| plain           | conversational | both          |      0.972 |               0.965 |   0.944 |   0.993 |       0.007 | 144 |
| plain           | long           | correct_first |      0.947 |               0.965 |   0.895 |   1     |       0.018 |  57 |
| plain           | long           | wrong_first   |      0.982 |               0.982 |   0.947 |   1     |       0     |  57 |
| plain           | long           | both          |      0.965 |               0.974 |   0.93  |   0.991 |       0.009 | 114 |
