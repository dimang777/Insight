#!/usr/bin/env python3
from flask import Flask, render_template, request

import sys
# Web_app
# sys.path.append('/home/ubuntu/application/data')

# Local
# sys.path.insert(0, './data')
from data import redwine_v3

# Create the application object
app = Flask(__name__)
rw = redwine_v3.RedWine('data/rw_df_mvp_v3.pkl', 'data/winetales_cos_dist_df_v2.pkl')

@app.route('/',methods=["GET","POST"])
def home_page():
    
    return render_template('index.html')  # render a template

@app.route('/output',methods=["GET"])
def tag_output():

    # Pull input
    id_num =request.args.get('user_input')
    id_cate =int(request.args.get('user_input2'))
    id_price =int(request.args.get('user_input3'))

    if id_price == 2:
        price_range = 10
    else:
        price_range = -1

    # Case if empty
    if id_num == '':
        return render_template("index.html",
                               my_input = id_num,
                               my_form_result="Empty")
    elif id_cate == 0:
        return render_template("index.html",
                               my_input = id_num,
                               my_form_result="Empty")
    elif id_cate == 0 and id_num == '':
        return render_template("index.html",
                               my_input = id_num,
                               my_form_result="Empty")
    else:
        if id_cate == 1:
            id_cate_result = 'L'
            id_type_display = 'LCBO#: '
        elif id_cate == 2:
            id_cate_result = 'V'
            id_type_display = 'Vintages#: '
        else:
            id_cate_result = 'Z'

        available_flag = rw.check_ifavailable(id_cate_result+str(id_num))

        if available_flag:
            [rangefound, recomm] = rw.get_recommendations(id_cate_result+str(id_num), price_range)
            product_available_str = 'Available'
            if rangefound:
                rangefound_str = 'Range_found'
                print(rangefound_str)
            else:
                rangefound_str = 'Range_notfound'
                print(rangefound_str)

            product_dict = rw.get_productinfo_in_dict(rw.get_idx_w_id(id_cate_result+str(id_num)))
            recomm_dict_list = []
            for idx in range(3):
                recomm_dict_list.append(rw.get_productinfo_in_dict(recomm[idx]))
    
            id_type_display_recomm = []
            for idx in range(3):
                if recomm_dict_list[idx]['LCBO_id'][0] == 'L':
                    id_type_display_recomm.append('LCBO#: ')
                else:
                    id_type_display_recomm.append('Vintages#: ')
    
    
            return render_template("index.html",
                                entered_product_info_name = product_dict['Name'],
                                entered_product_info_id = id_type_display + str(id_num),
                                entered_product_info_price = 'Price: ' + '$' + str(product_dict['Price']),
                                entered_product_info_size = 'Size: ' + str(product_dict['Size']) + 'mL',
                                entered_product_info_alcohol = 'Alcohol: ' + str(product_dict['Alcohol']) + '%',
                                entered_product_info_madein = 'Made in: ' + product_dict['Madein_city'] + ', ' + product_dict['Madein_country'],
                                entered_product_info_madeby = 'Made by: ' + product_dict['Brand'],
                                entered_product_info_sugar = 'Sugar: ' + str(product_dict['Sugar']) + 'g/L',
                                entered_product_info_sweetness = 'Sweetness: ' + product_dict['Sweetness'],
                                entered_product_info_style = 'Style: ' + product_dict['Style1'] + ', ' + product_dict['Style2'],
                                entered_product_info_variety = 'Variety: ' + product_dict['Variety'],
                                entered_product_info_img=product_dict['Pic_src'],
                                recomm_product_1_info_name = recomm_dict_list[0]['Name'],
                                recomm_product_1_info_id = id_type_display_recomm[0] + str(recomm_dict_list[0]['LCBO_id'][1:]),
                                recomm_product_1_info_price = 'Price: ' + '$' + str(recomm_dict_list[0]['Price']),
                                recomm_product_1_info_size = 'Size: ' + str(recomm_dict_list[0]['Size']) + 'mL',
                                recomm_product_1_info_alcohol = 'Alcohol: ' + str(recomm_dict_list[0]['Alcohol']) + '%',
                                recomm_product_1_info_madein = 'Made in: ' + recomm_dict_list[0]['Madein_city'] + ', ' + product_dict['Madein_country'],
                                recomm_product_1_info_madeby = 'Made by: ' + recomm_dict_list[0]['Brand'],
                                recomm_product_1_info_sugar = 'Sugar: ' + str(recomm_dict_list[0]['Sugar']) + 'g/L',
                                recomm_product_1_info_sweetness = 'Sweetness: ' + recomm_dict_list[0]['Sweetness'],
                                recomm_product_1_info_style = 'Style: ' + recomm_dict_list[0]['Style1'] + ', ' + recomm_dict_list[0]['Style2'],
                                recomm_product_1_info_variety = 'Variety: ' + recomm_dict_list[0]['Variety'],
                                recomm_product_1_info_img=recomm_dict_list[0]['Pic_src'],
                                recomm_product_2_info_name = recomm_dict_list[1]['Name'],
                                recomm_product_2_info_id = id_type_display_recomm[1] + str(recomm_dict_list[1]['LCBO_id'][1:]),
                                recomm_product_2_info_price = 'Price: ' + '$' + str(recomm_dict_list[1]['Price']),
                                recomm_product_2_info_size = 'Size: ' + str(recomm_dict_list[1]['Size']) + 'mL',
                                recomm_product_2_info_alcohol = 'Alcohol: ' + str(recomm_dict_list[1]['Alcohol']) + '%',
                                recomm_product_2_info_madein = 'Made in: ' + recomm_dict_list[1]['Madein_city'] + ', ' + product_dict['Madein_country'],
                                recomm_product_2_info_madeby = 'Made by: ' + recomm_dict_list[1]['Brand'],
                                recomm_product_2_info_sugar = 'Sugar: ' + str(recomm_dict_list[1]['Sugar']) + 'g/L',
                                recomm_product_2_info_sweetness = 'Sweetness: ' + recomm_dict_list[1]['Sweetness'],
                                recomm_product_2_info_style = 'Style: ' + recomm_dict_list[1]['Style1'] + ', ' + recomm_dict_list[1]['Style2'],
                                recomm_product_2_info_variety = 'Variety: ' + recomm_dict_list[1]['Variety'],
                                recomm_product_2_info_img=recomm_dict_list[1]['Pic_src'],
                                recomm_product_3_info_name = recomm_dict_list[2]['Name'],
                                recomm_product_3_info_id = id_type_display_recomm[2] + str(recomm_dict_list[2]['LCBO_id'][1:]),
                                recomm_product_3_info_price = 'Price: ' + '$' + str(recomm_dict_list[2]['Price']),
                                recomm_product_3_info_size = 'Size: ' + str(recomm_dict_list[2]['Size']) + 'mL',
                                recomm_product_3_info_alcohol = 'Alcohol: ' + str(recomm_dict_list[2]['Alcohol']) + '%',
                                recomm_product_3_info_madein = 'Made in: ' + recomm_dict_list[2]['Madein_city'] + ', ' + product_dict['Madein_country'],
                                recomm_product_3_info_madeby = 'Made by: ' + recomm_dict_list[2]['Brand'],
                                recomm_product_3_info_sugar = 'Sugar: ' + str(recomm_dict_list[2]['Sugar']) + 'g/L',
                                recomm_product_3_info_sweetness = 'Sweetness: ' + recomm_dict_list[2]['Sweetness'],
                                recomm_product_3_info_style = 'Style: ' + recomm_dict_list[2]['Style1'] + ', ' + recomm_dict_list[2]['Style2'],
                                recomm_product_3_info_variety = 'Variety: ' + recomm_dict_list[2]['Variety'],
                                recomm_product_3_info_img=recomm_dict_list[2]['Pic_src'],
                                my_form_result="NotEmpty",
                                product_available = product_available_str,
                                range_found = rangefound_str
                                )
        else:
            product_available_str = 'NotAvailable'
            recomm = []
            return render_template("index.html",
                               my_input = id_cate_result+str(id_num),
                               my_form_result="NotEmpty",
                               product_available = product_available_str)



# start the server with the 'run()' method
if __name__ == "__main__":
    # Local
    app.run(debug=True, host='0.0.0.0') #will run locally http://127.0.0.1:5000/
    # Web_app
    # app.run(host = "0.0.0.0",debug=True) #will run locally http://127.0.0.1:5000/

