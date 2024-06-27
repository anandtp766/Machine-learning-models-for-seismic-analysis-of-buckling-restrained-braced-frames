import PySimpleGUI as sg
import numpy as np
from joblib import dump, load

sg.theme('SystemDefault')	# Add color
b_inp1: dict = {'font':('Times New Roman', 12)}
b_inp2: dict = {'size':(26,1), 'font':('Times New Roman', 11)}
b_inp3: dict = {'size':(15,1), 'font':('Times New Roman', 11)}
b_inp4: dict = {'font':('Times New Roman', 12)}

# All the stuff inside your window.
layout = [  [sg.Text('Developed by T.P.Anand, Muhamed Safeer Pandikkadavath, Sujith Mangalathu, Dipti Ranjan Sahoo',**b_inp1)],             
            [sg.Frame(layout=[
            [sg.Text('Peak Ground Acceleration (g)',**b_inp2),sg.InputText(key='-f1-',**b_inp3),
             sg.Text('Spectral Acceleration at 1s (g)',**b_inp2), sg.InputText(key='-f7-',**b_inp3)],
            [sg.Text('Peak Ground Velocity (cm/s)',**b_inp2), sg.InputText(key='-f2-',**b_inp3),
             sg.Text('Spectral Acceleration at 2s (g)',**b_inp2),sg.InputText(key='-f8-',**b_inp3)],
            [sg.Text('Peak Ground Displacement (cm)',**b_inp2), sg.InputText(key='-f3-',**b_inp3),
             sg.Text('Spectral Acceleration at 3s (g)',**b_inp2),sg.InputText(key='-f9-',**b_inp3)],
            [sg.Text('Significant Duration (s)',**b_inp2), sg.InputText(key='-f4-',**b_inp3),
             sg.Text('Spectral Acceleration at 4s (g)',**b_inp2),sg.InputText(key='-f10-',**b_inp3)],
            [sg.Text('Arias Intensity (m/s)',**b_inp2), sg.InputText(key='-f5-',**b_inp3),
             sg.Text('Spectral Acceleration at 5s (g)',**b_inp2),sg.InputText(key='-f11-',**b_inp3)],
            [sg.Text('Mean Period (s) (g)',**b_inp2), sg.InputText(key='-f6-',**b_inp3),
             sg.Text('Height of Building (m)',**b_inp2),sg.InputText(key='-f14-',**b_inp3)],
            [sg.Text('Magnitude',**b_inp2),sg.InputText(key='-f12-',**b_inp3),
             sg.Text('Span (m)',**b_inp2),sg.InputText(key='-f15-',**b_inp3)],
            [sg.Text('Radius of rupture (km)',**b_inp2),sg.InputText(key='-f13-',**b_inp3),
             sg.Text('Total BRB area in apy frame (sq.cm)',**b_inp2),sg.InputText(key='-f16-',**b_inp3)]],
             title='Input Parameters',**b_inp4)],
            [sg.Frame(layout=[
            [sg.Text('IDR (%)',**b_inp2), sg.InputText(key='-OP1-',**b_inp3),
            sg.Text('Maximum Ductility Demand',**b_inp2), sg.InputText(key='-OP3-',**b_inp3)],
            [sg.Text('RDR (%)',**b_inp2), sg.InputText(key='-OP2-',**b_inp3),
            sg.Text('Cumulative Ductility Demand',**b_inp2), sg.InputText(key='-OP4-',**b_inp3)]],
            title='Engineering Demand Parameters (EDPs)',**b_inp4)],
            [sg.Button('Predict'),sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Estimation of EDPs of Buckling Restrained Braced Frames', layout=layout)

Parameter=['IDR','RDR','MaxDuc','CumDuc'];
loaded_model1 = load("XGboost_model_"+Parameter[0]+".pkl")
loaded_model2 = load("XGboost_model_"+Parameter[1]+".pkl")
loaded_model3 = load("XGboost_model_"+Parameter[2]+".pkl")
loaded_model4 = load("XGboost_model_"+Parameter[3]+".pkl")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	
        break
    if event == 'Predict':
        if values['-f1-'] == '' or values['-f2-'] == '' or values['-f3-'] == '' or values['-f4-'] == '' or values['-f5-'] == '' or values['-f6-'] == '' or values['-f7-'] == '' or values['-f8-'] == '' or values['-f9-'] == '' or values['-f10-'] == '' or values['-f11-'] == '' or values['-f12-'] == '' or values['-f13-'] == '' or values['-f14-'] == '' or values['-f15-'] == '' or values['-f16-'] == '':
            window['-OP-'].update('Please fill all the input parameters')
        else:
            x_test=np.array([[float(values['-f1-']),float(values['-f2-']), float(values['-f3-']),float(values['-f4-']),float(values['-f5-']),values['-f6-'],values['-f7-'],values['-f8-'],values['-f9-'],values['-f10-'],values['-f11-'],values['-f12-'],values['-f13-'],values['-f14-'],values['-f15-'],values['-f16-']]])
            x_test = x_test.astype(float)
            IDR = loaded_model1.predict(x_test)
            RDR = loaded_model2.predict(x_test)
            MaxDuc = loaded_model3.predict(x_test)
            CumDuc = loaded_model4.predict(x_test)
            window['-OP1-'].update(f'{IDR[0]:.3f}')                
            window['-OP2-'].update(f'{RDR[0]:.3f}')
            window['-OP3-'].update(f'{MaxDuc[0]:.3f}')
            window['-OP4-'].update(f'{CumDuc[0]:.3f}')
window.close()