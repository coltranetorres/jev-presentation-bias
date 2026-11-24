# Results summary

## Absolute grading (shift in P(correct) vs plain)

| side    | style          |   shift |   ci_lo |   ci_hi |   flip_rate |   n |
|:--------|:---------------|--------:|--------:|--------:|------------:|----:|
| correct | plain          |   0     |   0     |   0     |       0     |  38 |
| correct | reworded       |  -0.005 |  -0.031 |   0.016 |       0.053 |  38 |
| correct | formatted      |  -0.011 |  -0.022 |  -0.001 |       0.026 |  38 |
| correct | long           |  -0.032 |  -0.05  |  -0.016 |       0.031 |  32 |
| correct | short          |   0.026 |   0.003 |   0.051 |       0.026 |  38 |
| correct | confident      |  -0.089 |  -0.126 |  -0.056 |       0.088 |  34 |
| correct | technical      |  -0.006 |  -0.018 |   0.008 |       0.054 |  37 |
| correct | conversational |  -0.032 |  -0.059 |  -0.007 |       0.079 |  38 |
| wrong   | plain          |   0     |   0     |   0     |       0     |  38 |
| wrong   | reworded       |   0.022 |   0.006 |   0.04  |       0.053 |  38 |
| wrong   | formatted      |   0.021 |  -0.001 |   0.044 |       0.053 |  38 |
| wrong   | long           |   0.027 |   0.005 |   0.046 |       0.033 |  30 |
| wrong   | short          |   0.027 |   0.014 |   0.041 |       0.026 |  38 |
| wrong   | confident      |  -0.054 |  -0.084 |  -0.027 |       0.083 |  36 |
| wrong   | technical      |   0.016 |  -0.001 |   0.036 |       0.083 |  36 |
| wrong   | conversational |   0.005 |  -0.014 |   0.023 |       0.053 |  38 |


## Pairwise (accuracy, flips vs plain/plain)

| correct_style   | wrong_style    | order         |   accuracy |   baseline_accuracy |   ci_lo |   ci_hi |   flip_rate |   n |
|:----------------|:---------------|:--------------|-----------:|--------------------:|--------:|--------:|------------:|----:|
| plain           | plain          | correct_first |      0.892 |               0.892 |   0.784 |   0.973 |       0     |  37 |
| plain           | plain          | wrong_first   |      0.919 |               0.919 |   0.838 |   1     |       0     |  37 |
| plain           | plain          | both          |      0.905 |               0.905 |   0.838 |   0.959 |       0     |  74 |
| reworded        | plain          | correct_first |      0.865 |               0.892 |   0.757 |   0.973 |       0.027 |  37 |
| reworded        | plain          | wrong_first   |      0.919 |               0.919 |   0.838 |   1     |       0     |  37 |
| reworded        | plain          | both          |      0.892 |               0.905 |   0.811 |   0.959 |       0.014 |  74 |
| plain           | reworded       | correct_first |      0.865 |               0.892 |   0.757 |   0.973 |       0.027 |  37 |
| plain           | reworded       | wrong_first   |      0.919 |               0.919 |   0.838 |   1     |       0     |  37 |
| plain           | reworded       | both          |      0.892 |               0.905 |   0.811 |   0.959 |       0.014 |  74 |
| formatted       | plain          | correct_first |      0.811 |               0.892 |   0.676 |   0.919 |       0.081 |  37 |
| formatted       | plain          | wrong_first   |      0.946 |               0.919 |   0.865 |   1     |       0.027 |  37 |
| formatted       | plain          | both          |      0.878 |               0.905 |   0.797 |   0.946 |       0.054 |  74 |
| plain           | formatted      | correct_first |      0.892 |               0.892 |   0.784 |   0.973 |       0.054 |  37 |
| plain           | formatted      | wrong_first   |      0.919 |               0.919 |   0.838 |   1     |       0     |  37 |
| plain           | formatted      | both          |      0.905 |               0.905 |   0.838 |   0.959 |       0.027 |  74 |
| long            | plain          | correct_first |      0.806 |               0.871 |   0.677 |   0.935 |       0.065 |  31 |
| long            | plain          | wrong_first   |      0.903 |               0.903 |   0.806 |   1     |       0     |  31 |
| long            | plain          | both          |      0.855 |               0.887 |   0.758 |   0.935 |       0.032 |  62 |
| plain           | long           | correct_first |      0.867 |               0.9   |   0.733 |   0.967 |       0.033 |  30 |
| plain           | long           | wrong_first   |      0.9   |               0.933 |   0.767 |   1     |       0.033 |  30 |
| plain           | long           | both          |      0.883 |               0.917 |   0.8   |   0.95  |       0.033 |  60 |
| short           | plain          | correct_first |      0.838 |               0.892 |   0.703 |   0.946 |       0.162 |  37 |
| short           | plain          | wrong_first   |      0.946 |               0.919 |   0.865 |   1     |       0.027 |  37 |
| short           | plain          | both          |      0.892 |               0.905 |   0.824 |   0.959 |       0.095 |  74 |
| plain           | short          | correct_first |      0.919 |               0.892 |   0.838 |   1     |       0.027 |  37 |
| plain           | short          | wrong_first   |      0.946 |               0.919 |   0.865 |   1     |       0.027 |  37 |
| plain           | short          | both          |      0.932 |               0.905 |   0.878 |   0.986 |       0.027 |  74 |
| confident       | plain          | correct_first |      0.758 |               0.879 |   0.606 |   0.879 |       0.121 |  33 |
| confident       | plain          | wrong_first   |      0.818 |               0.909 |   0.697 |   0.939 |       0.091 |  33 |
| confident       | plain          | both          |      0.788 |               0.894 |   0.682 |   0.879 |       0.106 |  66 |
| plain           | confident      | correct_first |      0.917 |               0.889 |   0.833 |   1     |       0.028 |  36 |
| plain           | confident      | wrong_first   |      0.944 |               0.917 |   0.861 |   1     |       0.028 |  36 |
| plain           | confident      | both          |      0.931 |               0.903 |   0.861 |   0.986 |       0.028 |  72 |
| technical       | plain          | correct_first |      0.889 |               0.889 |   0.778 |   0.972 |       0     |  36 |
| technical       | plain          | wrong_first   |      0.917 |               0.917 |   0.833 |   1     |       0     |  36 |
| technical       | plain          | both          |      0.903 |               0.903 |   0.833 |   0.958 |       0     |  72 |
| plain           | technical      | correct_first |      0.861 |               0.889 |   0.75  |   0.972 |       0.028 |  36 |
| plain           | technical      | wrong_first   |      0.917 |               0.917 |   0.833 |   1     |       0     |  36 |
| plain           | technical      | both          |      0.889 |               0.903 |   0.819 |   0.958 |       0.014 |  72 |
| conversational  | plain          | correct_first |      0.784 |               0.892 |   0.649 |   0.919 |       0.108 |  37 |
| conversational  | plain          | wrong_first   |      0.919 |               0.919 |   0.838 |   1     |       0     |  37 |
| conversational  | plain          | both          |      0.851 |               0.905 |   0.77  |   0.932 |       0.054 |  74 |
| plain           | conversational | correct_first |      0.919 |               0.892 |   0.838 |   1     |       0.027 |  37 |
| plain           | conversational | wrong_first   |      0.919 |               0.919 |   0.838 |   1     |       0     |  37 |
| plain           | conversational | both          |      0.919 |               0.905 |   0.851 |   0.973 |       0.014 |  74 |
