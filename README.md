# Cálculo de distancia con visión artificial basado en la transformada de Hough

Este código fue diseñado para calcular la distancia aproximada a la real en centímetros que existen entre dos cobjetos circulares. Para ello, se usó como referencia de medida una hoja tamaño carta. Se proporcionó un valor deseado en pixeles a un lado de la hoja, y el otro lado fue calculado con la regla de tres.

Para aplicar la regla de tres, se supone que los lados de la hoja tamaño carta son **a** y **b** conocidos en centímetros, y **x** y **y** desconocidos en pixeles respectivamente. Se propone un valor ya sea de **x** o de **y**, y se compara de tal manera que si **a** en centímetros es **x** pixeles, ¿cuánto sería **y** en pixeles conociendo el valor de **b**? De esta manera se se haría el producto de **b** con **x**, dividiendo el resultado anterior por **a**; obteniendo el valor de **y**.

Ahora bien, con los datos contemplado anteriormente se realiza cada parte del código para obtener un buen resultado de la distancia. EL código puede ser usado con una cámara en tiempo real, el problema es que aún es muy sensible a interrupciones y este se detiene marcando error.
