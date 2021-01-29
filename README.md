# dermia_demo

**DEMO** de software de detección y clasificación de patologías dermatológicas. 

El core es una *Deep Residual Learning Network* [RESNET-50](https://arxiv.org/abs/1512.03385) (NN), empleando [PyTorch](https://pytorch.org).
La base de datos de entrenamiento se extrajo de *International Skin Imaging Collaboration* [ICIC](https://www.isic-archive.com).

## Software.

<img src="samples/img01.png" alt="drawing" width="500"/> <img src="samples/img02.png" alt="drawing" width="500"/>

El software es muy simple, se carga una imágen, mediante el botón 'Sel Img', se puede visualizar la imágen presionando `View Image`, mostrando la imágen cargada, como en la figura de la izquierda.
Presionando 'Procesar' la imágen entra a la NN y se muestran los resultados, ver la figura de derecha.

Si se cargan varias imágenes, se registran en el 'box' de selección superior, y si la red obtiene más de un resultado, estos se encuentran en el 'box' inferior.

De acuerdo con el corpus de ISIC, se detectan sólo dos categorías, **nevus** y **melanoma**. No hay mayores especificidades en el diagnóstico.

El entrenamiento de la red **NO** es exaustivo, el protocolo se definió en 50 épocas, buscando que F>1.2, y una probabilida de detección correcta por arriba de 0.9.

## Condiciones de desarrollo.

-Python 3.8




