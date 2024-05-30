## Summary

### Python Script: Entropy Calculations
**Author:** mohabhui  
**Date:** 26-Sep-2021

This Python script provides functions to calculate various types of entropy: Shannon entropy, joint entropy, and conditional entropy. It includes utilities to format and print data for better readability. The main function, `calcEntropy`, calculates and prints the entropy based on the provided data and the specified entropy type. Below is a summary of the key functions:

### Functions

1. **`rost(mydata)`**:
   - Rounds and converts a floating-point number to a string, rounded to 3 decimal places.

2. **`roli(mylist)`**:
   - Rounds each item in a list of floating-point numbers to 3 decimal places.

3. **`prettyPrintList(mylist)`**:
   - Prints a list of numbers in a formatted string with items rounded to 3 decimal places.

4. **`calcEntropy(pData, entropy='jointXY')`**:
   - Calculates and prints entropy based on the specified type: `independentX` (Shannon entropy), `jointXY` (joint entropy), `conditionalYX`, or `conditionalXY`.
   - Handles one-dimensional arrays for `independentX` and two-dimensional arrays for the other types.
   - Validates input and prints intermediate steps and results.

### Example Usage

The script provides example data sets and demonstrates how to call the `calcEntropy` function with different types of entropy:

```python
if __name__ == "__main__":
    data1 = [1/2, 1/4, 1/8, 1/8]
    data2 = [[0.1, 0, 0], [0.2, 0.3, 0.2],[0, 0, 0.2]]
    data3 = [[1/10, 1/20, 1/40, 1/80, 1/80], [1/20, 1/40, 1/80, 1/80, 1/10],[1/40, 1/80, 1/80, 1/10, 1/20], [1/80,1/80,1/10,1/20,1/40], [1/80,1/10,1/20,1/40,1/80]]
    data4v1 = [[1/8, 1/16, 1/32, 1/32],[1/16, 1/8, 1/32, 1/32],[1/16, 1/16, 1/16, 1/16],[1/4, 0, 0, 0]]
    data4v2 = [[0.125, 0.0625, 0.03125, 0.03125], [0.0625, 0.125, 0.03125, 0.03125], [0.0625, 0.0625, 0.0625, 0.0625], [0.25, 0, 0, 0]]
    data5 = [[24/100, 25/100], [1/100, 50/100]]

    # Example calls to calcEntropy
    calcEntropy(data1, 'independentX')
    calcEntropy(data2, 'jointXY')
    calcEntropy(data2, 'conditionalYX')
    calcEntropy(data2, 'conditionalXY')
    calcEntropy(data5, 'conditionalXY')
```

This script is useful for educational purposes and for anyone needing to calculate different types of entropy for probability data sets.