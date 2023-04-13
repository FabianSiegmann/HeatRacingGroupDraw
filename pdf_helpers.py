import fpdf

# Define handling mode of fonts for the fpdf module
fpdf.set_global("FPDF_CACHE_MODE", 1)

class PDF(fpdf.FPDF):
     pass # nothing happens when it is executed.

def create_PDF_GIKC_style(pdf):
    # Create DIN A5 page
    pdf.add_page()

    # Add background image 
    pdf.image('resources/background/background.jpg', x = 0, y = 0, w = 149, h = 210, type = '', link = '')
    pdf.image('resources/background/GIKC-logo.jpg', x = 0, y = 0, w = 149, h = 35, type = '', link = '')

    # Add Fonts
    pdf.add_font("FreeSans", style="", fname="resources/fonts/FreeSans.ttf", uni=True)
    pdf.add_font("FreeSansBold", style="", fname="resources/fonts/FreeSansBold.ttf", uni=True)  
    pdf.add_font("FreeSansOblique", style="", fname="resources/fonts/FreeSansOblique.ttf", uni=True)  

    return pdf


def create_personal_schedule(data, driver, races, NUMBER_OF_ROUNDS, HEATS_PER_ROUND, DRIVER_PER_HEAT):
    # Calculate a specific size factor to ensure that the group draw always fits on one page
    SIZE_FACTOR = 1 / DRIVER_PER_HEAT * 130

    # Create PDF in GIKC Style
    pdf = PDF(orientation='P', unit='mm', format='A5')
    pdf = create_PDF_GIKC_style(pdf)

    # Add Headline
    pdf.set_font('FreeSansBold', '', 22)
    pdf.write(30, "\n")
    pdf.write(16, 'GIKC Schedule: ' + driver + "\n\n")

    # Add content
    for round in range(1,NUMBER_OF_ROUNDS+1):
        pdf.set_font('FreeSans', '', 16)
        pdf.write(8, data[round]['race'] + " (")# + data[round]['time'] + "), Kart " + str(data[round]['kart']) + "\n\n")
        pdf.set_font('FreeSansOblique', '', 16)
        pdf.write(8, data[round]['time'])
        pdf.set_font('FreeSans', '', 16)
        pdf.write(8, " ), ")
        if 'Sunday' in data[round]['time']:
            pdf.set_font('FreeSans', '', 1)
            pdf.write(8, 36 * " ")
            pdf.set_font('FreeSans', '', 16)
        pdf.write(8,"Kart " + str(data[round]['kart']) + "\n\n")

    # Add driver's races

    for round in range(1,NUMBER_OF_ROUNDS+1):
        for heat in range(1, HEATS_PER_ROUND+1):
            if driver in list(races[round][heat]['driver'].keys()):   

                create_PDF_GIKC_style(pdf)

                # Add Headline
                pdf.set_font('FreeSansBold', '', 22)
                pdf.write(30, "\n")
                pdf.write(10, races[round][heat]['name'] + " (" + races[round][heat]['time'] + ")")
                pdf.write(8, "\n\n")

                # Add the races where the driver is participating and mark him with red
                for kart_num in range(1,DRIVER_PER_HEAT+1):
                    my_driver = list(races[round][heat]['driver'].keys())[list(races[round][heat]['driver'].values()).index(kart_num)]
                    pdf.set_font('FreeSansBold', '', 2 * SIZE_FACTOR + 1)
                    if driver == my_driver:                        
                        pdf.set_text_color(255,0,0) 
                    pdf.write(SIZE_FACTOR, "Kart " + str(kart_num))
                    pdf.set_font('FreeSans', '', 2 * SIZE_FACTOR + 1)
                    if kart_num < 10:
                        pdf.write(SIZE_FACTOR,":" + 7 * " " + my_driver +  "\n")
                    else:
                        pdf.write(SIZE_FACTOR,":" + 5 * " " + my_driver +  "\n")
                    pdf.set_text_color(0,0,0)




    # Save as PDF
    pdf.output('output/personal_schedules/' + driver + '.pdf','F')
    pdf.close()


def create_race_pdf(races, round, heat, DRIVER_PER_HEAT):
    # Calculate a specific size factor to ensure that the group draw always fits on one page
    SIZE_FACTOR = 1 / DRIVER_PER_HEAT * 130

    # Create PDF in GIKC Style
    pdf = PDF(orientation='P', unit='mm', format='A5')
    pdf = create_PDF_GIKC_style(pdf)

    # Add Headline
    pdf.set_font('FreeSansBold', '', 22)
    pdf.write(30, "\n")
    pdf.write(10, races[round][heat]['name'] + " (" + races[round][heat]['time'] + ")")
    pdf.write(8, "\n\n")

    # Add content
    for kart_num in range(1,DRIVER_PER_HEAT+1):
        driver = list(races[round][heat]['driver'].keys())[list(races[round][heat]['driver'].values()).index(kart_num)]
        pdf.set_font('FreeSansBold', '', 2 * SIZE_FACTOR + 1)
        pdf.write(SIZE_FACTOR, "Kart " + str(kart_num))
        pdf.set_font('FreeSans', '', 2 * SIZE_FACTOR + 1)
        if kart_num < 10:
            pdf.write(SIZE_FACTOR,":" + 7 * " " + driver +  "\n")
        else:
            pdf.write(SIZE_FACTOR,":" + 5 * " " + driver +  "\n")
                
    # Save as PDF
    pdf.output('output/heats/' + races[round][heat]['name'] + '.pdf','F')
    pdf.close()