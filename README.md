# dermia_demo

**DEMO** de software de detección y clasificación de patologías dermatológicas. 

El core es una *Deep Residual Learning Network* [RESNET-50](https://arxiv.org/abs/1512.03385) (NN), empleando [PyTorch](https://pytorch.org).
El corpus de entrenamiento se extrajo de *International Skin Imaging Collaboration* [ICIC](https://www.isic-archive.com).

## Interfaz de Usuario.

<img src="samples/img01.png" alt="drawing" width="500"/> 
<img src="samples/img02.png" alt="drawing" width="500"/>

El Interfaz es muy simple, se carga una imágen, mediante el botón `Sel Img`, y se puede visualizar presionando `View Image`(ver figura superior).
Presionando `Procesar` la imágen entra a la NN, y se detectan y clasifican tales detecciones. Los resultados se muestran al finalizar (ver la figura inferior)

Para hacer un poco más dinámica la interfaz, se implementaton dos cajas de selección (`box`). Mediante `box` superior se pueden seleccionar las imágenes cargadas con `Sel Img`. `box` inferior permite seleccionar los resultados arrojados por la NN para la imagen seleccionada.

Se detectan sólo dos categorías, **nevus** y **melanoma**, no hay mayores especificidades en el diagnóstico. Esta limitante está dada por el corpus de ISIC. 



## Condiciones de testeo.
Se desarrolló empleando:

- Python 3.8 (no emplear Python 3.9)
- Torch 1.6.0
- Torchvision 0.7.0
- Matplotlib 3.3.2
- PyQt5 5.15.1
- numpy 1.19.2

Es importante tener en cuenta que, si se corre en OSX Catalina, tiene Python 3.9, y Pytorch no es estable con esa versión de Python. Y en particular, en este caso, no anda.

El entrenamiento de la red **NO** es exaustivo, el protocolo se definió en 50 épocas, buscando que F>1.2, y una probabilida de detección correcta por arriba de 0.9.

## Corpus.
Se bajaron 2400 imágenes de ICIC, lamentablemente, sólo el 6% de esas imágenes (144) corresponden a **melanomas**, y por lo tanto el corpus tiene un bias importante. Para entrenar la red, se generó un corpus de 288 elementos, compuesto por los **144 melanomas** y **144 nevus** elegidos en forma aleatoria. Por cada época de entrenamiento, se elegían nuevas imágenes correspondientes a nevus. Desde ya, esta estrategia genera un overfitting de los melanomas en relación a los nevus.
Otra opción es no renovar los nevus en cada epoca, lo que reduce el corpus a 288 elementos. Para los fines prácticos del demostrador, es útil también.

## Parámetros.
En el repo no se encuentran los parámetros de la red, se deben descargar y mover al directorio `model/'.  
- [ISICModel_parameters.pt](https://drive.google.com/file/d/1tMS0KXOhvCH4UiPTf-nt093U0OG3gmf9/view?usp=sharing)





