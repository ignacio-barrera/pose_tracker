
### FeetTracker::stepCriteriaAdvanced
Determina si se ha producido un paso evaluando desplazamientos en x e y. Considera desplazamientos insignificantes y cambios de orientación en el desplazamiento.

Linea 1580-1617 mcp-vision-detection/src/lib/FeetTracker.cpp

```
bool FeetTracker::stepCriteriaAdvanced(int index, int Dx, int Dy, bool left) {
    if(abs(Dx) < min_displacement && abs(Dy) < min_displacement) { //Evident case, no significant movement
        if(left) {
            last_step_left_idx = index;
            last_step_left_bbox = left_rects_s[index];
        } else {
            last_step_right_idx = index;
            last_step_right_bbox = right_rects_s[index];
        }
        return true;
    } else if(index > 0) { //Check displacement orientation change
        //Flags for sign change
        if(abs(Dy) < min_displacement) { //Insignificant y displacement
            if(orientation_change(index, Dx, left, true)) { //If x orientation changes, means a step occured
                if(left) {
                    last_step_left_idx = index;
                    last_step_left_bbox = left_rects_s[index];
                } else {
                    last_step_right_idx = index;
                    last_step_right_bbox = right_rects_s[index];
                }
                return true;
            }
        } else { //Significant y displacement: check if it changes signs significantly (shall be a step)
            if(orientation_change(index, Dy, left, false)) { //If orientation changes, means
                if(left) {
                    last_step_left_idx = index;
                    last_step_left_bbox = left_rects_s[index];
                } else {
                    last_step_right_idx = index;
                    last_step_right_bbox = right_rects_s[index];
                }
                return true;
            }
        }
    }
    return false;
}
```
#### Parámetros:
- int index: Numero de frame actual
- int Dx: Variación de posición en x (Smooth)
- int Dy: Variación de posición en y (Smooth)
- bool left: Indica que pie se evalua, True para left, False para right


### FeetTracker::orientation_change
Verifica si ha habido un cambio de orientación en el desplazamiento acumulado de una serie de fotogramas anteriores al índice actual.

Linea 1558-1578 mcp-vision-detection/src/lib/FeetTracker.cpp

```
bool FeetTracker::orientation_change(int index, int value, bool left, bool is_x) {
    if(value == 0)
        return false;
    int d, acc_d=0, i, last_step_idx = left ? last_step_left_idx : last_step_right_idx,
        crit = (last_step_idx == -1) ? 0 : last_step_idx;

    std::vector<int>& D = left ? (is_x ? Dx_left_s : Dy_left_s) : (is_x ? Dx_right_s : Dy_right_s);

    for(i=index-1; i>=crit; --i) {
        d = D[i];
        acc_d += d;
        if(d == 0)
            continue;
        if ((value>0 && d<0) || (value<0 && d>0)) {
            if(abs(acc_d) > min_displacement)
        return true;
        }
    }

    return false;
}
```

#### Parámetros:
- int index: Numero de frame actual
- int value: Variación de posición en x
- bool left: Indica que pie se evalua, True para left, False para right
- bool is_x: Indica en que dirección se evalua, True para x, False para y


### FeetTracker::smoothDisplacement
El código suaviza las variaciones de posición de los pies usando una media ponderada de hasta cinco fotogramas: el fotograma actual, hasta dos fotogramas anteriores y hasta dos fotogramas posteriores. Los pesos {4, 2, 1} indican que el fotograma actual tiene la mayor influencia (peso 4), seguido por el primer fotograma vecino (peso 2) y luego el segundo fotograma vecino (peso 1). Este enfoque proporciona un balance entre suavizar las variaciones y mantener la fidelidad de los datos originales, especialmente dando más importancia al fotograma actual.

Transforma los Dx_left, Dy_left, Dx_right, Dy_right a Dx_left_s, Dy_left_s, Dx_right_s, Dy_right_s.

Linea 1481-1506 mcp-vision-detection/src/lib/FeetTracker.cpp

´´´
void FeetTracker::smoothDisplacement(int index)
{
    float sum_dx_left = weights[0] * Dx_left[index], sum_dy_left = weights[0] * Dy_left[index],
          sum_dx_right = weights[0] * Dx_right[index], sum_dy_right = weights[0] * Dy_right[index];
    int s = Dx_left.size(), norm = weights[0];
    for (int i = index + 1, j = 1; i < s && j <= 2; ++i, ++j)
    {
        sum_dx_left += weights[j] * Dx_left[i];
        sum_dy_left += weights[j] * Dy_left[i];
        sum_dx_right += weights[j] * Dx_right[i];
        sum_dy_right += weights[j] * Dy_right[i];
        norm += weights[j];
    }
    for (int i = index - 1, j = 1; i >= 0 && j <= 2; --i, ++j)
    {
        sum_dx_left += weights[j] * Dx_left[i];
        sum_dy_left += weights[j] * Dy_left[i];
        sum_dx_right += weights[j] * Dx_right[i];
        sum_dy_right += weights[j] * Dy_right[i];
        norm += weights[j];
    }
    Dx_left_s[index] = sum_dx_left / norm;
    Dy_left_s[index] = sum_dy_left / norm;
    Dx_right_s[index] = sum_dx_right / norm;
    Dy_right_s[index] = sum_dy_right / norm;
}
´´´

#### Parámetros:
- int index: Numero de frame actual

### Variables utilizadas:

```
int index; //Frame number
std::vector<int> Dx_left; //Position variation from previous frame in x for left foot
std::vector<int> Dy_left; //Position variation from previous frame in y for left foot
std::vector<int> Dx_right; //Position variation from previous frame in x for right foot
std::vector<int> Dy_right; //Position variation from previous frame in y for right foot
std::vector<int> Dx_left_s; //Smooth position variation from previous frame in x for left foot
std::vector<int> Dy_left_s; //Smooth position variation from previous frame in y for left foot
std::vector<int> Dx_right_s; //Smooth position variation from previous frame in x for right foot
std::vector<int> Dy_right_s; //Smooth position variation from previous frame in y for right foot
const int FeetTracker::weights[3] = {4, 2, 1}; //Weights for Smooth steps (4 for actual frame, 2 for one frame after, 1 for two frames after, the same for the two frames before)
int last_step_left_idx; //ID of the last frame with a detected step for the left foot
int last_step_right_idx; //ID of the last frame with a detected step for the left foot
``` 
