This solver can simulate convective flows in rectangular cavities in three main configurations:  

# 1- Sidewall convection
In order to simulate the flow in a side wall heated and cooled cavity one needs to activate it by assigning sidewall Rayleigh number, for example:

```python
params.Ra_side = 1e5
```
In this case, it is possible to have different configuration based on the dimension of the problem and boundary conditions:

## 2D

To activate 2D configuration one needs to assign:
```python
params.oper.dim = 2
```
We have two possiblities:

1- **Insulated walls in y direction**

The default is insulated horizontal walls.

2- **Periodic boundary conditions in y direction**

One should assign:

```python
params.oper.y_periodicity = True
```

## 3D

To activate 3D configuration one needs to assign:
```python
params.oper.dim = 3
```
We have three possiblities:

1- **Insulated walls in y and z directions**

The default is insulated walls in two other directions.

2- **Periodic boundary conditions in z direction**

One should assign:

```python
params.oper.z_periodicity = True
```

In this case, we have periodic boundary conditions in z direction and insulated walls in y direction.

3- **Periodic boundary conditions in y and z direction** 

One should assign:

```python
params.oper.y_periodicity = True
params.oper.z_periodicity = True
```


# 2- Rayleigh-Bénard convection

In order to simulate the flow in a Rayleigh-Bénard cavity (bottom plate heated and top cooled) one needs to activate it by assigning vertical Rayleigh number, for example: 

```python
params.Ra_vert = 1750
```

In this case, it is possible to have different configuration based on the dimension of the problem and boundary conditions:

## 2D

To activate 2D configuration one needs to assign:
```python
params.oper.dim = 2
```
We have two possiblities:

1- **Insulated walls in x direction**

The default is insulated vertical walls.

2- **Periodic boundary conditions in x direction**

One should assign:

```python
params.oper.x_periodicity = True
```

## 3D

To activate 3D configuration one needs to assign:
```python
params.oper.dim = 3
```
We have three possiblities:

1- **Insulated walls in x and z directions**

The default is insulated walls in two other directions.

2- **Periodic boundary conditions in z direction**

One should assign:

```python
params.oper.z_periodicity = True
```

In this case, we have periodic boundary conditions in z direction and insulated walls in x direction.

3- **Periodic boundary conditions in x and z direction** 

One should assign:

```python
params.oper.x_periodicity = True
params.oper.z_periodicity = True
```

# 3- Mixed case (sidewall convection + Rayleigh-Bénard convection)

In order to simulate the flow in a cavity that both sidewalls and horizontal ones are differentially heated and cooled, one needs to to activate it by assigning both sidewall and vertical Rayleigh numbers, for example:
```python
params.Ra_side = 5000
params.Ra_vert = 5000
```
In this case, it is possible to have different configuration based on the dimension of the problem and boundary conditions:

## 2D

To activate 2D configuration one needs to assign:
```python
params.oper.dim = 2
```
## 3D

To activate 3D configuration one needs to assign:
```python
params.oper.dim = 3
```
We have two possiblities:

1- **Insulated walls in z direction**

The default is insulated walls in z direction.

2- **Periodic boundary conditions in z direction**

One should assign:

```python
params.oper.z_periodicity = True
```

In this case, we have periodic boundary conditions in z direction.