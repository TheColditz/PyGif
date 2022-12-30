import PySimpleGUI as sg
import imageio
from PIL import Image
from PIL import UnidentifiedImageError

# Layout
sg.theme('LightBrown1')

layout = [[sg.Text('Select images to include in the animated GIF:')],
          [sg.Input(key="Input"), sg.FileBrowse()],
          [sg.Button('Add'), sg.Button('Remove')],
          [sg.Listbox(values=[], size=(100, 20), key='image_list')],
          [sg.Text('Delay between images (in seconds):'), sg.InputText(default_text='0.1', key="Delay")],
          [sg.Text('Final resolution (width x height):'), sg.InputText(default_text='320x240', key="Resolution")],
          [sg.Button('Create Animated GIF')]]

window = sg.Window('PyGif').Layout(layout)

images = []
delay = 0.1

while True:
    event, values = window.Read()

    if event is None:
        break
    elif event == 'Add':
        images.append(values['Input'])
        window["image_list"].Update(images)

    elif event == 'Remove':
        images.remove(values['image_list'][0])
        window.FindElement('image_list').Update(images)

    elif event == 'Create Animated GIF':
        try:
            delay = float(values['Delay'].replace(",", "."))
            width, height = map(int, values['Resolution'].split('x'))

            resized_images = []
            for image in images:
                with Image.open(image) as im:
                    im = im.resize((width, height))
                    resized_images.append(im)

            imageio.mimsave('animated.gif', resized_images, duration=delay)
            sg.Popup('Animated GIF created!')
        except ValueError:
            sg.Popup("Incorrect dimensions given...\n\n"
                     "use 'width'x'height'\n"
                     "(e.g. 320x240)")
        except UnidentifiedImageError:
            sg.Popup("Cannot identify image file...\n\n"
                     "Please make sure the files you added are valid image files")

window.Close()
