# MapOfTheMostVisitedSkyAreas
An attempt to build the map of the most visited sky areas by astrophotographers on the Astrobin community

This is a work in progress and for the time being I just created a template csv file that is supposed to simulate the input data coming from Astrobin, with astrometry data and field of view.

This data is processed trough a few lines of Python code and generate circles whose size will represent the field of view of the picture and whose center is carefully placed over a sky chart (that has been made from sources found on Internet : careful about using them...). I am using openCV library to perform that quickly.

Now the radius of circles is not at the correct size, for test purposes (I have too few inputs to make something sexy out of it yet :-). I am also wondering if I should distort the circles in order to account for deformation of geometry in the vicinity of the poles ? Maybe in future versions...

I haven't yet normalized the picture : will do it with more data to adjust color and make nice "heat maps".

To be continued...

#Season 2
After a first good test with 1000 of images infos and plotting red circles on the positions of the images, we adapted the little Python code to draw rectangles with shape and size fitting the info from the pictures.
I also took into account for the distortion of the map from equator to the poles, when drawing the field of view.
2 flavours now : red shades or heat map, that needs some tweaking...

![Result](https://astrob.in/e4clel/0/)
