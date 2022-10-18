# Сheck Your Code Against the Following Points

### 1. Use `count()` method

Use `count()` method instead of `.aggregate()` with `Count()`

Good example:
```python
Model.oblects.filter(field=value).count()
```

Bad example:
```python
Model.oblects.filter(field=value).aggregate(Count("id"))
```

### 2. Don't use f-string for string type

Good example:
```python
Model.oblects.filter(field=value)
```

Bad example:
```python
Model.oblects.filter(field=f"{value}")
```

### 3. Don't forget to fix code-style

#### 1) Choose good variable names

For example, `lst` is a bad variable name.

#### 2) Check for correct line wrapping

Good example:
```python
queryset = list(
        Model.objects.filter(
            Q(long_field__nested__icontains="a") 
            | Q(second_long_field__nested__icontains="b")
        ).distinct()
    )
```

Bad example:
```python
queryset = list(Model.objects.filter(Q(long_field__nested__icontains="a")|Q(second_long_field__nested__icontains="b")).distinct())
```

#### 3) Make one-line function, if it possible

```python
def return_list() -> list[Model]:
    return list(
            Model.objects.filter(
                Q(long_field__nested__icontains="a") 
                | Q(second_long_field__nested__icontains="b")
            ).distinct()
        )
```

Bad example:
```python
def return_list() -> list[Model]:
    queryset = list(
        Model.objects.filter(
            Q(long_field__nested__icontains="a") 
            | Q(second_long_field__nested__icontains="b")
        ).distinct()
    )
    list_query = list(queryset)
    return list_query
```


### 4. Don't confuse the meaning of `select_related` and `prefetch_related`

- `select_related` usually used for `1-to-n` relations(such as `ForeignKey`).
- `prefetch_related` used for `n-to-n` relations(`ManyToMany`).

### 5. Don't use additional methods if it unneeded

Good example:
```python
Model.objects.prefetch_related("field")
```

Bad example:
```python
Model.objects.all().prefetch_related("field")
```

