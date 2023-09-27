#!/usr/bin/env python3

import sys
import argparse
import json
import ipaddress
import urllib.parse
import http.client
import pygal

countries = {}
continents = {}

pygal_supported_countries = [{"country_code":"ad","country_name":"Andorra"},{"country_code":"ae","country_name":"United Arab Emirates"},{"country_code":"af","country_name":"Afghanistan"},{"country_code":"al","country_name":"Albania"},{"country_code":"am","country_name":"Armenia"},{"country_code":"ao","country_name":"Angola"},{"country_code":"aq","country_name":"Antarctica"},{"country_code":"ar","country_name":"Argentina"},{"country_code":"at","country_name":"Austria"},{"country_code":"au","country_name":"Australia"},{"country_code":"az","country_name":"Azerbaijan"},{"country_code":"ba","country_name":"Bosnia and Herzegovina"},{"country_code":"bd","country_name":"Bangladesh"},{"country_code":"be","country_name":"Belgium"},{"country_code":"bf","country_name":"Burkina Faso"},{"country_code":"bg","country_name":"Bulgaria"},{"country_code":"bh","country_name":"Bahrain"},{"country_code":"bi","country_name":"Burundi"},{"country_code":"bj","country_name":"Benin"},{"country_code":"bn","country_name":"Brunei Darussalam"},{"country_code":"bo","country_name":"Bolivia, Plurinational State of"},{"country_code":"br","country_name":"Brazil"},{"country_code":"bt","country_name":"Bhutan"},{"country_code":"bw","country_name":"Botswana"},{"country_code":"by","country_name":"Belarus"},{"country_code":"bz","country_name":"Belize"},{"country_code":"ca","country_name":"Canada"},{"country_code":"cd","country_name":"Congo, the Democratic Republic of the"},{"country_code":"cf","country_name":"Central African Republic"},{"country_code":"cg","country_name":"Congo"},{"country_code":"ch","country_name":"Switzerland"},{"country_code":"ci","country_name":"Cote d’Ivoire"},{"country_code":"cl","country_name":"Chile"},{"country_code":"cm","country_name":"Cameroon"},{"country_code":"cn","country_name":"China"},{"country_code":"co","country_name":"Colombia"},{"country_code":"cr","country_name":"Costa Rica"},{"country_code":"cu","country_name":"Cuba"},{"country_code":"cv","country_name":"Cape Verde"},{"country_code":"cy","country_name":"Cyprus"},{"country_code":"cz","country_name":"Czech Republic"},{"country_code":"de","country_name":"Germany"},{"country_code":"dj","country_name":"Djibouti"},{"country_code":"dk","country_name":"Denmark"},{"country_code":"do","country_name":"Dominican Republic"},{"country_code":"dz","country_name":"Algeria"},{"country_code":"ec","country_name":"Ecuador"},{"country_code":"ee","country_name":"Estonia"},{"country_code":"eg","country_name":"Egypt"},{"country_code":"eh","country_name":"Western Sahara"},{"country_code":"er","country_name":"Eritrea"},{"country_code":"es","country_name":"Spain"},{"country_code":"et","country_name":"Ethiopia"},{"country_code":"fi","country_name":"Finland"},{"country_code":"fr","country_name":"France"},{"country_code":"ga","country_name":"Gabon"},{"country_code":"gb","country_name":"United Kingdom"},{"country_code":"ge","country_name":"Georgia"},{"country_code":"gf","country_name":"French Guiana"},{"country_code":"gh","country_name":"Ghana"},{"country_code":"gl","country_name":"Greenland"},{"country_code":"gm","country_name":"Gambia"},{"country_code":"gn","country_name":"Guinea"},{"country_code":"gq","country_name":"Equatorial Guinea"},{"country_code":"gr","country_name":"Greece"},{"country_code":"gt","country_name":"Guatemala"},{"country_code":"gu","country_name":"Guam"},{"country_code":"gw","country_name":"Guinea-Bissau"},{"country_code":"gy","country_name":"Guyana"},{"country_code":"hk","country_name":"Hong Kong"},{"country_code":"hn","country_name":"Honduras"},{"country_code":"hr","country_name":"Croatia"},{"country_code":"ht","country_name":"Haiti"},{"country_code":"hu","country_name":"Hungary"},{"country_code":"id","country_name":"Indonesia"},{"country_code":"ie","country_name":"Ireland"},{"country_code":"il","country_name":"Israel"},{"country_code":"in","country_name":"India"},{"country_code":"iq","country_name":"Iraq"},{"country_code":"ir","country_name":"Iran, Islamic Republic of"},{"country_code":"is","country_name":"Iceland"},{"country_code":"it","country_name":"Italy"},{"country_code":"jm","country_name":"Jamaica"},{"country_code":"jo","country_name":"Jordan"},{"country_code":"jp","country_name":"Japan"},{"country_code":"ke","country_name":"Kenya"},{"country_code":"kg","country_name":"Kyrgyzstan"},{"country_code":"kh","country_name":"Cambodia"},{"country_code":"kp","country_name":"Korea, Democratic People’s Republic of"},{"country_code":"kr","country_name":"Korea, Republic of"},{"country_code":"kw","country_name":"Kuwait"},{"country_code":"kz","country_name":"Kazakhstan"},{"country_code":"la","country_name":"Lao People’s Democratic Republic"},{"country_code":"lb","country_name":"Lebanon"},{"country_code":"li","country_name":"Liechtenstein"},{"country_code":"lk","country_name":"Sri Lanka"},{"country_code":"lr","country_name":"Liberia"},{"country_code":"ls","country_name":"Lesotho"},{"country_code":"lt","country_name":"Lithuania"},{"country_code":"lu","country_name":"Luxembourg"},{"country_code":"lv","country_name":"Latvia"},{"country_code":"ly","country_name":"Libyan Arab Jamahiriya"},{"country_code":"ma","country_name":"Morocco"},{"country_code":"mc","country_name":"Monaco"},{"country_code":"md","country_name":"Moldova, Republic of"},{"country_code":"me","country_name":"Montenegro"},{"country_code":"mg","country_name":"Madagascar"},{"country_code":"mk","country_name":"Macedonia, the former Yugoslav Republic of"},{"country_code":"ml","country_name":"Mali"},{"country_code":"mm","country_name":"Myanmar"},{"country_code":"mn","country_name":"Mongolia"},{"country_code":"mo","country_name":"Macao"},{"country_code":"mr","country_name":"Mauritania"},{"country_code":"mt","country_name":"Malta"},{"country_code":"mu","country_name":"Mauritius"},{"country_code":"mv","country_name":"Maldives"},{"country_code":"mw","country_name":"Malawi"},{"country_code":"mx","country_name":"Mexico"},{"country_code":"my","country_name":"Malaysia"},{"country_code":"mz","country_name":"Mozambique"},{"country_code":"na","country_name":"Namibia"},{"country_code":"ne","country_name":"Niger"},{"country_code":"ng","country_name":"Nigeria"},{"country_code":"ni","country_name":"Nicaragua"},{"country_code":"nl","country_name":"Netherlands"},{"country_code":"no","country_name":"Norway"},{"country_code":"np","country_name":"Nepal"},{"country_code":"nz","country_name":"New Zealand"},{"country_code":"om","country_name":"Oman"},{"country_code":"pa","country_name":"Panama"},{"country_code":"pe","country_name":"Peru"},{"country_code":"pg","country_name":"Papua New Guinea"},{"country_code":"ph","country_name":"Philippines"},{"country_code":"pk","country_name":"Pakistan"},{"country_code":"pl","country_name":"Poland"},{"country_code":"pr","country_name":"Puerto Rico"},{"country_code":"ps","country_name":"Palestine, State of"},{"country_code":"pt","country_name":"Portugal"},{"country_code":"py","country_name":"Paraguay"},{"country_code":"re","country_name":"Reunion"},{"country_code":"ro","country_name":"Romania"},{"country_code":"rs","country_name":"Serbia"},{"country_code":"ru","country_name":"Russian Federation"},{"country_code":"rw","country_name":"Rwanda"},{"country_code":"sa","country_name":"Saudi Arabia"},{"country_code":"sc","country_name":"Seychelles"},{"country_code":"sd","country_name":"Sudan"},{"country_code":"se","country_name":"Sweden"},{"country_code":"sg","country_name":"Singapore"},{"country_code":"sh","country_name":"Saint Helena, Ascension and Tristan da Cunha"},{"country_code":"si","country_name":"Slovenia"},{"country_code":"sk","country_name":"Slovakia"},{"country_code":"sl","country_name":"Sierra Leone"},{"country_code":"sm","country_name":"San Marino"},{"country_code":"sn","country_name":"Senegal"},{"country_code":"so","country_name":"Somalia"},{"country_code":"sr","country_name":"Suriname"},{"country_code":"st","country_name":"Sao Tome and Principe"},{"country_code":"sv","country_name":"El Salvador"},{"country_code":"sy","country_name":"Syrian Arab Republic"},{"country_code":"sz","country_name":"Swaziland"},{"country_code":"td","country_name":"Chad"},{"country_code":"tg","country_name":"Togo"},{"country_code":"th","country_name":"Thailand"},{"country_code":"tj","country_name":"Tajikistan"},{"country_code":"tl","country_name":"Timor-Leste"},{"country_code":"tm","country_name":"Turkmenistan"},{"country_code":"tn","country_name":"Tunisia"},{"country_code":"tr","country_name":"Turkey"},{"country_code":"tw","country_name":"Taiwan (Republic of China)"},{"country_code":"tz","country_name":"Tanzania, United Republic of"},{"country_code":"ua","country_name":"Ukraine"},{"country_code":"ug","country_name":"Uganda"},{"country_code":"us","country_name":"United States"},{"country_code":"uy","country_name":"Uruguay"},{"country_code":"uz","country_name":"Uzbekistan"},{"country_code":"va","country_name":"Holy See (Vatican City State)"},{"country_code":"ve","country_name":"Venezuela, Bolivarian Republic of"},{"country_code":"vn","country_name":"Viet Nam"},{"country_code":"ye","country_name":"Yemen"},{"country_code":"yt","country_name":"Mayotte"},{"country_code":"za","country_name":"South Africa"},{"country_code":"zm","country_name":"Zambia"},{"country_code":"zw","country_name":"Zimbabwe"}]

countries_continents = [{"country_code":"ad","continent":"Europe"},{"country_code":"ae","continent":"Asia"},{"country_code":"af","continent":"Asia"},{"country_code":"al","continent":"Europe"},{"country_code":"am","continent":"Europe"},{"country_code":"ao","continent":"Africa"},{"country_code":"aq","continent":"Antarctica"},{"country_code":"ar","continent":"South America"},{"country_code":"at","continent":"Europe"},{"country_code":"au","continent":"Oceania"},{"country_code":"az","continent":"Asia"},{"country_code":"az","continent":"Europe"},{"country_code":"ba","continent":"Europe"},{"country_code":"bd","continent":"Asia"},{"country_code":"be","continent":"Europe"},{"country_code":"bf","continent":"Africa"},{"country_code":"bg","continent":"Europe"},{"country_code":"bh","continent":"Asia"},{"country_code":"bi","continent":"Africa"},{"country_code":"bj","continent":"Africa"},{"country_code":"bn","continent":"Asia"},{"country_code":"bo","continent":"South America"},{"country_code":"br","continent":"South America"},{"country_code":"bt","continent":"Asia"},{"country_code":"bw","continent":"Africa"},{"country_code":"by","continent":"Europe"},{"country_code":"bz","continent":"North America"},{"country_code":"ca","continent":"North America"},{"country_code":"cd","continent":"Africa"},{"country_code":"cf","continent":"Africa"},{"country_code":"cg","continent":"Africa"},{"country_code":"ch","continent":"Europe"},{"country_code":"ci","continent":"Africa"},{"country_code":"cl","continent":"South America"},{"country_code":"cm","continent":"Africa"},{"country_code":"cn","continent":"Asia"},{"country_code":"co","continent":"South America"},{"country_code":"cr","continent":"North America"},{"country_code":"cu","continent":"North America"},{"country_code":"cv","continent":"Africa"},{"country_code":"cy","continent":"Europe"},{"country_code":"cz","continent":"Europe"},{"country_code":"de","continent":"Europe"},{"country_code":"dj","continent":"Africa"},{"country_code":"dk","continent":"Europe"},{"country_code":"do","continent":"North America"},{"country_code":"dz","continent":"Africa"},{"country_code":"ec","continent":"South America"},{"country_code":"ee","continent":"Europe"},{"country_code":"eg","continent":"Africa"},{"country_code":"eh","continent":"Africa"},{"country_code":"er","continent":"Africa"},{"country_code":"es","continent":"Europe"},{"country_code":"et","continent":"Africa"},{"country_code":"fi","continent":"Europe"},{"country_code":"fr","continent":"Europe"},{"country_code":"ga","continent":"Africa"},{"country_code":"gb","continent":"Europe"},{"country_code":"ge","continent":"Asia"},{"country_code":"ge","continent":"Europe"},{"country_code":"gf","continent":"South America"},{"country_code":"gh","continent":"Africa"},{"country_code":"gl","continent":"North America"},{"country_code":"gm","continent":"Africa"},{"country_code":"gn","continent":"Africa"},{"country_code":"gq","continent":"Africa"},{"country_code":"gr","continent":"Europe"},{"country_code":"gt","continent":"North America"},{"country_code":"gu","continent":"Oceania"},{"country_code":"gw","continent":"Africa"},{"country_code":"gy","continent":"South America"},{"country_code":"hk","continent":"Asia"},{"country_code":"hn","continent":"North America"},{"country_code":"hr","continent":"Europe"},{"country_code":"ht","continent":"North America"},{"country_code":"hu","continent":"Europe"},{"country_code":"id","continent":"Asia"},{"country_code":"ie","continent":"Europe"},{"country_code":"il","continent":"Asia"},{"country_code":"in","continent":"Asia"},{"country_code":"iq","continent":"Asia"},{"country_code":"ir","continent":"Asia"},{"country_code":"is","continent":"Europe"},{"country_code":"it","continent":"Europe"},{"country_code":"jm","continent":"North America"},{"country_code":"jo","continent":"Asia"},{"country_code":"jp","continent":"Asia"},{"country_code":"ke","continent":"Africa"},{"country_code":"kg","continent":"Asia"},{"country_code":"kh","continent":"Asia"},{"country_code":"kp","continent":"Asia"},{"country_code":"kr","continent":"Asia"},{"country_code":"kw","continent":"Asia"},{"country_code":"kz","continent":"Asia"},{"country_code":"kz","continent":"Europe"},{"country_code":"la","continent":"Asia"},{"country_code":"lb","continent":"Asia"},{"country_code":"li","continent":"Europe"},{"country_code":"lk","continent":"Asia"},{"country_code":"lr","continent":"Africa"},{"country_code":"ls","continent":"Africa"},{"country_code":"lt","continent":"Europe"},{"country_code":"lu","continent":"Europe"},{"country_code":"lv","continent":"Europe"},{"country_code":"ly","continent":"Africa"},{"country_code":"ma","continent":"Africa"},{"country_code":"mc","continent":"Europe"},{"country_code":"md","continent":"Europe"},{"country_code":"me","continent":"Europe"},{"country_code":"mg","continent":"Africa"},{"country_code":"mk","continent":"Europe"},{"country_code":"ml","continent":"Africa"},{"country_code":"mm","continent":"Asia"},{"country_code":"mn","continent":"Asia"},{"country_code":"mo","continent":"Asia"},{"country_code":"mr","continent":"Africa"},{"country_code":"mt","continent":"Europe"},{"country_code":"mu","continent":"Africa"},{"country_code":"mv","continent":"Asia"},{"country_code":"mw","continent":"Africa"},{"country_code":"mx","continent":"North America"},{"country_code":"my","continent":"Asia"},{"country_code":"mz","continent":"Africa"},{"country_code":"na","continent":"Africa"},{"country_code":"ne","continent":"Africa"},{"country_code":"ng","continent":"Africa"},{"country_code":"ni","continent":"North America"},{"country_code":"nl","continent":"Europe"},{"country_code":"no","continent":"Europe"},{"country_code":"np","continent":"Asia"},{"country_code":"nz","continent":"Oceania"},{"country_code":"om","continent":"Asia"},{"country_code":"pa","continent":"North America"},{"country_code":"pe","continent":"South America"},{"country_code":"pg","continent":"Oceania"},{"country_code":"ph","continent":"Asia"},{"country_code":"pk","continent":"Asia"},{"country_code":"pl","continent":"Europe"},{"country_code":"pr","continent":"North America"},{"country_code":"ps","continent":"Asia"},{"country_code":"pt","continent":"Europe"},{"country_code":"py","continent":"South America"},{"country_code":"re","continent":"Africa"},{"country_code":"ro","continent":"Europe"},{"country_code":"rs","continent":"Europe"},{"country_code":"ru","continent":"Asia"},{"country_code":"ru","continent":"Europe"},{"country_code":"rw","continent":"Africa"},{"country_code":"sa","continent":"Asia"},{"country_code":"sc","continent":"Africa"},{"country_code":"sd","continent":"Africa"},{"country_code":"se","continent":"Europe"},{"country_code":"sg","continent":"Asia"},{"country_code":"sh","continent":"Africa"},{"country_code":"si","continent":"Europe"},{"country_code":"sk","continent":"Europe"},{"country_code":"sl","continent":"Africa"},{"country_code":"sm","continent":"Europe"},{"country_code":"sn","continent":"Africa"},{"country_code":"so","continent":"Africa"},{"country_code":"sr","continent":"South America"},{"country_code":"st","continent":"Africa"},{"country_code":"sv","continent":"North America"},{"country_code":"sy","continent":"Asia"},{"country_code":"sz","continent":"Africa"},{"country_code":"td","continent":"Africa"},{"country_code":"tg","continent":"Africa"},{"country_code":"th","continent":"Asia"},{"country_code":"tj","continent":"Asia"},{"country_code":"tl","continent":"Asia"},{"country_code":"tm","continent":"Asia"},{"country_code":"tn","continent":"Africa"},{"country_code":"tr","continent":"Asia"},{"country_code":"tr","continent":"Europe"},{"country_code":"tw","continent":"Asia"},{"country_code":"tz","continent":"Africa"},{"country_code":"ua","continent":"Europe"},{"country_code":"ug","continent":"Africa"},{"country_code":"us","continent":"North America"},{"country_code":"uy","continent":"South America"},{"country_code":"uz","continent":"Asia"},{"country_code":"va","continent":"Europe"},{"country_code":"ve","continent":"South America"},{"country_code":"vn","continent":"Asia"},{"country_code":"ye","continent":"Asia"},{"country_code":"yt","continent":"Africa"},{"country_code":"za","continent":"Africa"},{"country_code":"zm","continent":"Africa"},{"country_code":"zw","continent":"Africa"}]

def is_valid_ip(ip):
    try:
        ipaddress_object = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', metavar='Your IP2Location.io API key.')
    parser.add_argument('-f', '--file', metavar='Your Nginx/Apache log file.')
    parser.add_argument('-m', '--mode', metavar='Type of map to be generated.')
    parser.add_argument('-o', '--outputfile', metavar='Your SVG filename.')

    return parser

def findkeys(value):
    for dict__ in pygal_supported_countries:
        if dict__["country_code"] == value:
            return dict__
    return None

def findkeys_continents(value):
    for dict__ in countries_continents:
        if dict__["country_code"] == value:
            return dict__
    return None

def ip2locationio_lookup(key, ip_address, language=''):
    if is_valid_ip(ip_address):
        parameters = urllib.parse.urlencode((("key", key), ("ip", ip_address), ("format", "json"), ("lang", language)))
        conn = http.client.HTTPSConnection("api.ip2location.io")
        conn.request("GET", "/?" + parameters)
        res = conn.getresponse()
        response = json.loads(res.read())
        return response
    else:
        print("Invalid IP address detected.")

def generate_svg_map(filename, apikey, mode, output_filename):
    try:
        entries_notsupported_count = 0
        
        file1 = open(filename, 'r')
        Lines = file1.readlines()
     
        print("Lookup for geolocation information from IP2Location.io API..." + "\n")

        for line in Lines:
            split1 = line.strip().split(' ')
            ip = split1[0]
            if ip != '':
                result = ip2locationio_lookup(apikey, ip)
                if mode == "world":
                    if findkeys(result["country_code"].lower()):
                        cname = findkeys(result["country_code"].lower())["country_name"]
                        if result["country_code"].lower() in countries:
                            countries[result["country_code"].lower()] = [countries[result["country_code"].lower()][0] + 1, cname]
                        else:
                            countries[result["country_code"].lower()] = [1, cname]
                    else:
                        entries_notsupported_count = entries_notsupported_count + 1
                elif mode == "continent":
                    if findkeys_continents(result["country_code"].lower()):
                        continentname = findkeys_continents(result["country_code"].lower())["continent"]
                        if continentname in continents:
                            continents[continentname] = [continents[continentname][0] + 1, continentname]
                        else:
                            continents[continentname] = [1, continentname]
                    else:
                        entries_notsupported_count = entries_notsupported_count + 1
                else:
                    print("Invalid mode detected.")
                    return
        
        if entries_notsupported_count > 0:
            print("Note: %i entries are not supported due to origin country did not supported by pygal." % entries_notsupported_count)
        
        # Plot SVG map
        print("Generating the SVG map..." + "\n")
        if mode == "world":
            worldmap_chart = pygal.maps.world.World()
            worldmap_chart.title = "Distribution of IP addresses in log files by country"
            for country in countries:
                worldmap_chart.add(countries[country][1], {country: countries[country][0]})
            worldmap_chart.render_to_file(output_filename)
        elif mode == "continent":
            supra = pygal.maps.world.SupranationalWorld()
            for continent in continents:
                supra.add(continents[continent][1], [(continents[continent][1].lower().replace(' ', '_'), continents[continent][0])])
            supra.render_to_file(output_filename)
        print("Generated the SVG map..." + "\n")
        
    except FileNotFoundError:
        print("Log file not found.")

if __name__ == '__main__':
    is_help = False
    # print(sys.argv)
    if len(sys.argv) >= 2:
        # for index, arg in enumerate(sys.argv):
            # if arg in ['--help', '-h', '-?']:
                # print_usage()
                # is_help = True
        if is_help is False:
            parser = create_parser()
            args = parser.parse_args(sys.argv[1:])
            # print(args)
            if args.mode is None:
                mode = "world"
            else:
                mode = args.mode
            if args.outputfile is None:
                outputfile = "map.svg"
            else:
                outputfile = args.outputfile
            if args.key is not None and args.file is not None:
                generate_svg_map(args.file, args.key, mode, outputfile)
            elif args.key is None:
                print("Missing API key.")
            elif args.file is None:
                print("Missing log file.")
    else:
        print("Missing parameters. Please enter 'ip2location.io -h' for more information.")