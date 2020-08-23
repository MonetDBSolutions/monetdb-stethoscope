import random

planets = [
	'Mercury',
	'Venus',
	'Earth',
	'Mars',
	'Jupiter',
	'Saturn',
	'Uranus',
	'Neptune',
	'Pluto'
    ]

# Only small, single word country names are used for obfuscation
countries= [
    'Afghanistan',
    'Albania',
    # 'American_Samoa',
    'Andorra',
    'Angola',
    'Anguilla',
    # 'Antigua_and_Barbuda',
    'Argentina',
    'Armenia',
    'Aruba',
    'Australia',
    'Austria',
    'Bahamas',
    'Bahrain',
    'Bangladesh',
    'Barbados',
    'Belgium',
    'Belize',
    'Benin',
    'Bermuda',
    'Bhutan',
    'Bolivia',
    # 'Bosnia_and_Herzegovina',
    'Botswana',
    'Brazil',
    'Brunei',
    'Bulgaria',
    # 'Burkina_Faso',
    'Cambodia',
    'Cameroon',
    'Canada',
    # 'Cape_Verde',
    # 'Cayman_Islands',
    'Chile',
    'China',
    'Colombia',
    'Congo',
    # 'Costa_Rica',
    'Croatia',
    'Cyprus',
    # 'Czech_Republic',
    'Denmark',
    'Dominica',
    # 'Dominican_Republic',
    'Ecuador',
    'Egypt',
    # 'El_Salvador',
    # 'Equatorial_Guinea',
    'Eritrea',
    'Ethiopia',
    # 'Faroe_Islands',
    'Fiji',
    'Finland',
    'France',
    # 'French_Guiana',
    # 'French_Polynesia',
    'Georgia',
    'Germany',
    'Ghana',
    'Gibraltar',
    'Greece',
    'Grenada',
    'Guadeloupe',
    'Guam',
    'Guatemala',
    'Guyana',
    'Haiti',
    'Honduras',
    'Hong_Kong',
    'Hungary',
    'Iceland',
    'India',
    'Indonesia',
    'Iran',
    'Iraq',
    'Ireland',
    'Italy',
    'Ivory_Coast',
    'Jamaica',
    'Japan',
    'Jordan',
    'Kazakhstan',
    'Kenya',
    'Kuwait',
    'Kyrgyzstan',
    'Laos',
    'Latvia',
    'Lebanon',
    'Lesotho',
    'Libya',
    'Liechtenstein',
    'Lithuania',
    'Luxembourg',
    'Macao',
    'Malawi',
    'Malaysia',
    'Malta',
    'Marshall_Islands',
    'Martinique',
    'Mauritius',
    'Mayotte',
    'Mexico',
    'Micronesia',
    'Moldova',
    'Monaco',
    'Mongolia',
    'Montserrat',
    'Mozambique',
    'Myanmar',
    'Namibia',
    'Nepal',
    'Netherlands',
    # 'Netherlands_Antilles',
    # 'New_Caledonia',
    # 'New_Zealand',
    'Nicaragua',
    'Niger',
    'Nigeria',
    'Norway',
    'Oman',
    'Pakistan',
    'Palestine',
    'Panama',
    'Paraguay',
    'Peru',
    'Philippines',
    'Poland',
    'Portugal',
    'Puerto_Rico',
    'Qatar',
    'Reunion',
    'Romania',
    'Russia',
    'Rwanda',
    # 'Saint_Kitts_and_Nevis',
    # 'Saint_Lucia',
    # 'Saint_Vincent_and_The_Grenadines',
    # 'Saudi_Arabia',
    'Serbia',
    'Singapore',
    'Slovakia',
    'Slovenia',
    # 'South_Africa',
    # 'South_Korea',
    'Spain',
    # 'Sri_Lanka',
    'Sudan',
    # 'Sudan_South',
    'Suriname',
    'Swaziland',
    'Sweden',
    'Switzerland',
    'Syria',
    'Taiwan',
    'Tajikistan',
    'Tanzania',
    'Thailand',
    # 'Trinidad_and_Tobago',
    'Turkey',
    'Turkmenistan',
    # 'Turks_and_Caicos_Islands',
    'Uganda',
    'Ukraine',
    # 'United_Kingdom',
    # 'United_States',
    # 'United_States_Virgin_Islands',
    'Uruguay',
    'Uzbekistan',
    'Vatican',
    'Venezuela',
    'Vietnam',
    'Wallis_and_Futuna',
    'Yemen',
    ]


class ObfuscateTransformer:
    """The default is to replace every literal value in the plan with three asterisks."""
    schema_mapping= {}
    table_mapping= {}
    column_mapping= {}

    def __init__(self):
        # The types which we are censoring
        self._types = [
            # "bit",
            "bte",
            "sht",
            "int",
            "lng",
            "hge",
            "oid",
            "flt",
            "dbl",
            "str",
            "color",
            "date",
            "daytime",
            "time",
            "timestamp",
            "timezone",
            "blob",
            "inet",
            "url",
            "json"
        ]

    # obfuscation is MAL instruction specific
    def __call__(self, json_object):
        rdict = dict(json_object)

        # map schema information
        if rdict['module'] == 'sql' and (rdict['function'] == 'bind' or rdict['function'] = 'bind_idx'):
            var[2]["value"] = self.obfuscate_schema(var[2]["value"])
            var[3]["value"] = self.obfuscate_table(var[3]["value"])
            var[4]["value"] = self.obfuscate_column(var[4]["value"])
            continue

        # map selections and arithmetics
        elif rdict['module'] == 'algebra' and rdict['function'] == 'thetaselect':
            var[3]["value"] = self.obfuscate_data(var[3]["value"], var[3]["type"])

        elif rdict['module'] == 'algebra' and rdict['function'] == 'select':
            var[3]["value"] = self.obfuscate_data(var[3]["value"], var[3]["type"])
            var[4]["value"] = self.obfuscate_data(var[4]["value"], var[4]["type"])
        
        else:
            for var in rdict.get("args", []):
                # hide the table information
                alias = var.get("alias")
                s,t,c = alias.split('.')
                s = self.obfuscate_schema(s)
                t = self.obfuscate_table(s)
                c = self.obfuscate_column(s)
                var["alias"] = '.'.join([s,t,c])
        return rdict

    def obfuscate_schema(original):
        if original in schema_mapping:
            return schema_mapping[original]
        picked = random.choose(planets)
        schema_mapping.update({original: picked})
        del planets[picked]
        return picked

    def obfuscate_table(original):
        if original in table_mapping:
            return table_mapping[original]
        picked = random.choose(countries)
        table_mapping.update({original: picked})
        del planets[picked]
        return picked


    def obfuscate_column(original):
        if original in column_mapping:
            return column_mapping[original]
        picked = "col_"+str(len(column_mapping))
        column_mapping.update({original: picked})
        return picked

    def obfuscate_data(original, tpe):
        # should be refined
        if tpe == ':str':
            picked = '***'
        else:
            picked = original
        return picked
