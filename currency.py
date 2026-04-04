import re
import os
import sys
import argparse
import requests

available_currencies = {
    'AED': 'UAE Dirham',
    'AFN': 'Afghan Afghani',
    'ALL': 'Albanian Lek',
    'AMD': 'Armenian Dram',
    'ANG': 'Netherlands Antillian Guilder',
    'AOA': 'Angolan Kwanza',
    'ARS': 'Argentine Peso',
    'AUD': 'Australian Dollar',
    'AWG': 'Aruban Florin',
    'AZN': 'Azerbaijani Manat',
    'BAM': 'Bosnia and Herzegovina Mark',
    'BBD': 'Barbados Dollar',
    'BDT': 'Bangladeshi Taka',
    'BGN': 'Bulgarian Lev',
    'BHD': 'Bahraini Dinar',
    'BIF': 'Burundian Franc',
    'BMD': 'Bermudian Dollar',
    'BND': 'Brunei Dollar',
    'BOB': 'Bolivian Boliviano',
    'BRL': 'Brazilian Real',
    'BSD': 'Bahamian Dollar',
    'BTN': 'Bhutanese Ngultrum',
    'BWP': 'Botswana Pula',
    'BYN': 'Belarusian Ruble',
    'BZD': 'Belize Dollar',
    'CAD': 'Canadian Dollar',
    'CDF': 'Congolese Franc',
    'CHF': 'Swiss Franc',
    'CLF': 'Chilean Unidad de Fomento',
    'CLP': 'Chilean Peso',
    'CNH': 'Offshore Chinese Renminbi',
    'CNY': 'Chinese Renminbi',
    'COP': 'Colombian Peso',
    'CRC': 'Costa Rican Colon',
    'CUP': 'Cuban Peso',
    'CVE': 'Cape Verdean Escudo',
    'CZK': 'Czech Koruna',
    'DJF': 'Djiboutian Franc',
    'DKK': 'Danish Krone',
    'DOP': 'Dominican Peso',
    'DZD': 'Algerian Dinar',
    'EGP': 'Egyptian Pound',
    'ERN': 'Eritrean Nakfa',
    'ETB': 'Ethiopian Birr',
    'EUR': 'Euro',
    'FJD': 'Fiji Dollar',
    'FKP': 'Falkland Islands Pound',
    'FOK': 'Faroese Króna',
    'GBP': 'Pound Sterling',
    'GEL': 'Georgian Lari',
    'GGP': 'Guernsey Pound',
    'GHS': 'Ghanaian Cedi',
    'GIP': 'Gibraltar Pound',
    'GMD': 'Gambian Dalasi',
    'GNF': 'Guinean Franc',
    'GTQ': 'Guatemalan Quetzal',
    'GYD': 'Guyanese Dollar',
    'HKD': 'Hong Kong Dollar',
    'HNL': 'Honduran Lempira',
    'HRK': 'Croatian Kuna',
    'HTG': 'Haitian Gourde',
    'HUF': 'Hungarian Forint',
    'IDR': 'Indonesian Rupiah',
    'ILS': 'Israeli New Shekel',
    'IMP': 'Manx Pound',
    'INR': 'Indian Rupee',
    'IQD': 'Iraqi Dinar',
    'ISK': 'Icelandic Króna',
    'JEP': 'Jersey Pound',
    'JMD': 'Jamaican Dollar',
    'JOD': 'Jordanian Dinar',
    'JPY': 'Japanese Yen',
    'KES': 'Kenyan Shilling',
    'KGS': 'Kyrgyzstani Som',
    'KHR': 'Cambodian Riel',
    'KID': 'Kiribati Dollar',
    'KMF': 'Comorian Franc',
    'KRW': 'South Korean Won',
    'KWD': 'Kuwaiti Dinar',
    'KYD': 'Cayman Islands Dollar',
    'KZT': 'Kazakhstani Tenge',
    'LAK': 'Lao Kip',
    'LBP': 'Lebanese Pound',
    'LKR': 'Sri Lanka Rupee',
    'LRD': 'Liberian Dollar',
    'LSL': 'Lesotho Loti',
    'LYD': 'Libyan Dinar',
    'MAD': 'Moroccan Dirham',
    'MDL': 'Moldovan Leu',
    'MGA': 'Malagasy Ariary',
    'MKD': 'Macedonian Denar',
    'MMK': 'Burmese Kyat',
    'MNT': 'Mongolian Tögrög',
    'MOP': 'Macanese Pataca',
    'MRU': 'Mauritanian Ouguiya',
    'MUR': 'Mauritian Rupee',
    'MVR': 'Maldivian Rufiyaa',
    'MWK': 'Malawian Kwacha',
    'MXN': 'Mexican Peso',
    'MYR': 'Malaysian Ringgit',
    'MZN': 'Mozambican Metical',
    'NAD': 'Namibian Dollar',
    'NGN': 'Nigerian Naira',
    'NIO': 'Nicaraguan Córdoba',
    'NOK': 'Norwegian Krone',
    'NPR': 'Nepalese Rupee',
    'NZD': 'New Zealand Dollar',
    'OMR': 'Omani Rial',
    'PAB': 'Panamanian Balboa',
    'PEN': 'Peruvian Sol',
    'PGK': 'Papua New Guinean Kina',
    'PHP': 'Philippine Peso',
    'PKR': 'Pakistani Rupee',
    'PLN': 'Polish Złoty',
    'PYG': 'Paraguayan Guaraní',
    'QAR': 'Qatari Riyal',
    'RON': 'Romanian Leu',
    'RSD': 'Serbian Dinar',
    'RUB': 'Russian Ruble',
    'RWF': 'Rwandan Franc',
    'SAR': 'Saudi Riyal',
    'SBD': 'Solomon Islands Dollar',
    'SCR': 'Seychellois Rupee',
    'SDG': 'Sudanese Pound',
    'SEK': 'Swedish Krona',
    'SGD': 'Singapore Dollar',
    'SHP': 'Saint Helena Pound',
    'SLE': 'Sierra Leonean Leone',
    'SOS': 'Somali Shilling',
    'SRD': 'Surinamese Dollar',
    'SSP': 'South Sudanese Pound',
    'STN': 'São Tomé and Príncipe Dobra',
    'SYP': 'Syrian Pound',
    'SZL': 'Eswatini Lilangeni',
    'THB': 'Thai Baht',
    'TJS': 'Tajikistani Somoni',
    'TMT': 'Turkmenistan Manat',
    'TND': 'Tunisian Dinar',
    'TOP': 'Tongan Paʻanga',
    'TRY': 'Turkish Lira',
    'TTD': 'Trinidad and Tobago Dollar',
    'TVD': 'Tuvaluan Dollar',
    'TWD': 'New Taiwan Dollar',
    'TZS': 'Tanzanian Shilling',
    'UAH': 'Ukrainian Hryvnia',
    'UGX': 'Ugandan Shilling',
    'USD': 'United States Dollar',
    'UYU': 'Uruguayan Peso',
    'UZS': "Uzbekistani So'm",
    'VES': 'Venezuelan Bolívar Soberano',
    'VND': 'Vietnamese Đồng',
    'VUV': 'Vanuatu Vatu',
    'WST': 'Samoan Tālā',
    'XAF': 'Central African CFA Franc',
    'XCD': 'East Caribbean Dollar',
    'XDR': 'Special Drawing Rights',
    'XOF': 'West African CFA franc',
    'XPF': 'CFP Franc',
    'YER': 'Yemeni Rial',
    'ZAR': 'South African Rand',
    'ZMW': 'Zambian Kwacha',
    'ZWL': 'Zimbabwean Dollar'
}

class CurrencyApp:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser('currency', description='convert different currencies')
        self.parser.add_argument('input', help='input in format of "100 eur to usd"')
        self.parser.add_argument('-l', '--list', action='store_true',help='return list of available currencies')

        self.current_currency = ''
        self.target_currency = ''
        self.count = 0
    
    def parse_currency_input(self, text) -> None:
        pattern = r'^\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]{3})\s+to\s+([a-zA-Z]{3})\s*$'
        match = re.match(pattern, text.strip(), re.IGNORECASE)
    
        if not match:
            raise ValueError('Invalid format. Expected format like "10 eur to usd"')
    
        self.count = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
        self.current_currency = match.group(2).upper()
        self.target_currency = match.group(3).upper()  

    def send_api_request(self) -> float:
        api_key = os.getenv('CURRENCY_API_KEY')
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{self.current_currency}'
        response = requests.api.get(url).json()
        
        multiplier = response['conversion_rates'][self.target_currency]
        result = round(self.count * multiplier, 2)
        return result
    
    def list_available_currencies(self):
        print('All available currencies:')
        for key in available_currencies:
            print(f'{key}: {available_currencies[key]}')

app = CurrencyApp()
args = app.parser.parse_args()

if __name__ == '__main__':
    if args.list:
        app.list_available_currencies()
        sys.exit(0)
    
    app.parse_currency_input(args.input)
    result = app.send_api_request()

    print(f'{app.count} {app.current_currency} to {app.target_currency} = {result} {app.target_currency}')
    