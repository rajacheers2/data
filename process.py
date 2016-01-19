import csv, urllib, os, subprocess
def read_csv():
    path = '/home/raja/Downloads/fashion_test - Sheet1.csv'
    csvreader = csv.reader(open(path, 'rb'), delimiter=',', quotechar='|')
    for idx, row in enumerate(csvreader):
        if idx == 0:
            continue
        url = row[0]
        yield url

def download_images():
    path = '/home/raja/dev/data/original_images'
    for idx, url in enumerate(read_csv()):
        print idx, url  
        img_path = os.path.join(path, str(idx)+'.jpg')
        urllib.urlretrieve(url, img_path)

def run_masks():
    path = '/home/raja/dev/data/results/'
    for idx, url in enumerate(read_csv()):
        directory = os.path.join(path, str(idx))
        if not os.path.exists(directory):
            os.makedirs(directory)
        orig_img_path = os.path.join('/home/raja/dev/data/original_images', str(idx)+'.jpg')
        formatted_command =  "./feature_gen "+orig_img_path + " LOCATION BRAND 0 " + directory + "/ 0 localhost iqnect iqpass fashion features_top_bottom -v >" + os.path.join(directory, 'out.txt')
        print formatted_command
        subprocess.call(formatted_command, shell=True)
        

def get_img_html(directory, img_name):
    return '<img src="'+os.path.join(os.path.join(directory,img_name+'.jpg'))+'" width=200 style="margin: 3">'
    
def write_html():
    look = {
        'model_type':{
            '0':'Half body',
            '1':'Full Body'},
        'img_tag':{
            '1':'waist',
            '2':'knee',
            '3':'full',
            '4':'undefined'},
        'item_tag':{
            '1':'top',
            '2':'bottom',
            '3':'dress',
            '4':'undefined'},
        'sleeve_type':{
            '1':'sleeveless',
            '2':'short',
            '3':'half',
            '4':'long',
            '5':'undefined'}}

    html_file = open('/home/raja/dev/data/myfile.html','w')
    h = ''
    path = '/home/raja/dev/data/results/'
    for idx, url in enumerate(read_csv()):
        print "Idx : ", idx
        directory = os.path.join(path, str(idx))
        
        txt_file = open(os.path.join(directory,'out.txt'))
        lines = txt_file.readlines()
        html = ''
        try:
            
            html += "<h3>"+url+"</h3>"
            html += "Model Type : " + look['model_type'][lines[4][0]] + '<br>' 
            html += "Image tag : " + look['img_tag'][lines[5][0]] + '<br>' 
            #html += "Item tag : " + look['item_tag'][lines[6][0]] + '<br>' 
            #html += "Separation : " + lines[7][:-1] + '<br>'
            html += "Sleeve type : " + look['sleeve_type'][lines[16][0]] + '<br>' 
            html+= get_img_html(directory, 'orig')
            html+= get_img_html(directory, 'lineofsep')
            #html+= get_img_html(directory, 'pose')
            #html+= get_img_html(directory, 'prelimmask')
            html+= get_img_html(directory, 'skinmask')
            #html+= '<br>'
            #html+= 'Masks  <br>'
            #html += "Img type : " + look['item_tag'][lines[10][0]] + '<br>' 
            #html += "Item type : " + look['item_tag'][lines[12][0]] + '<br>' 
            #html += "Sleeve type : " + look['sleeve_type'][lines[16][0]] + '<br>' 
            
            if 'Feature starting' in lines[23]:
                
                #html+= 'Masks 2 <br>'
                #html += "Img type : " + look['item_tag'][lines[25][0]] + '<br>' 
                #html += "Item type : " + look['item_tag'][lines[27][0]] + '<br>' 
                #html += "Sleeve type : " + look['sleeve_type'][lines[31][0]] + '<br>' 
                
                #html+= 'Masks 3<br>'
                #html += "Img type : " + look['item_tag'][lines[40][0]] + '<br>' 
                #html += "Item type : " + look['item_tag'][lines[42][0]] + '<br>' 
                #html += "Sleeve type : " + look['sleeve_type'][lines[46][0]] + '<br>' 
                html+= get_img_html(directory, '2mask')
                html+= get_img_html(directory, '0mask')
                html+= get_img_html(directory, '1mask')
                
            else:
                html+= get_img_html(directory, '0mask')
            html+= '<br>'
        except Exception as e:
            print e
            pass
        h +=html
    html_file.write(h) 
    html_file.close()      
if __name__ == "__main__":
    #download_images()
    #run_masks()
    write_html()