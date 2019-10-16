DNA_Storage
===
## # Introduction

### 1 Prospect

### 2 Constraints

### 3 Existing Works

### 4 Thesis

---

## # GC-Content and Run-Length Constraint

### 1 Method Overview
Not to make things too complex at the very beginning, it is reasonable to consider only GC-content and run-length constraints since these two are mentioned and considered by most other studies.

Wentu Song et al. have come up with a method that can (only) satisfy these two constraints and can theoretically reach the highest code rate of $\frac{2n-1}{2n}$ [Ref]. The main idea of this method is staright forward. It simply tries to enumerate  elements in $Z_{4}^{n}$ that satisfies run-length constraint with as less as possiable GC-content distance. GC-content distance is defined as the absolute value of the difference between GC-content and 0.5. By enumerating in this way, it is expected that at least $2^{2n-1}$ elements can be found such that all the elements in $Z_{2}^{2n-1}$ can be mapped to a subset of $Z_{4}^{n}$, which actually generates an encoding table.


### 2 Procedure

### 3 Implementation and Test

---

## # LT Code

### In progress...

---

## # Future Plan

### [1 LT Code]

### 2 Further Test

### 3 Improve Performance