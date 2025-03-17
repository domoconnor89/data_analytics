import csv
import logging
import time
import re
import urllib3
import io
import pandas as pd
import requests
import json
import tempfile

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#### Core Setup Methods ####

class StudioEquipmentScraper:
    def __init__(
        self,
        max_workers: int = 1,
        rate_limit_delay: float = 4.7,
        batch_size: int = 30,
        verify_ssl: bool = True,
        use_selenium: bool = True,
        max_pages_per_studio: int = 20
    ):
        self.max_workers = max_workers
        self.rate_limit_delay = rate_limit_delay
        self.batch_size = batch_size
        self.verify_ssl = verify_ssl
        self.use_selenium = use_selenium
        self.visited_urls = set()  # Global URL cache
        self.url_scores = {}  # Cache for URL scores
        self.max_pages_per_studio = max_pages_per_studio

        
        # Equipment-related keywords (expanded)
        self.url_keywords = {
            'equipment', 'gear', 'tech', 'hardware', 'spec', 'specs','specification','specifications',
            'control room', 'studio', 'studios', 'live room', 'tracking', 'isolation booth', 'recording', 
            'equipment list', 'gear list', 'inventory','facilities', 'resources', 'setup',
            'instruments', 'microphones', 'microphone', 'equip', 'technik', 
            'plugins', 'plug-ins', 'outboard', 'backline', 'desk', 'console', 'deck', 'decks',
            'monitoring', 'monitors', 'speakers', 
            'equalizer', 'equaliser','compressors', 'kompressor', 
            'processors', 'pre-amps', 'preamps', 
            'tube', 'dynamic', 'condensers', 'ribbon', 'valve'
        }
        
        self.equipment_hierarchy = {
            'acoustic energy': ['ae2'],
            'adam': ['a7'],
            'adl': ['1000'],
            'adr': ['compex 2'],
            'aea': ['ku5a', 'r84', 'r84a', 'r88', 'r88 mk ii', 'a440', 'rpq500'],
            'akg': ['414','454','c12', 'c12vr', 'c28b', 'c3000', 'c414', 'c414 eb', 'c414b-uls', 
                    'c414-xls', 'c414b-xls','c451', 'c451b', 'c451e', 'd112', 'd112e', 
                    'd12e', 'd224', 'd196','bx25', 'the tube'],
            'alan smart': ['c1', 'c2'],
            'alesis': ['adats', 'quadraverb', 'midiverb ii', '3630'],
            'altec': ['rs124'],
            'amek': ['9098', '9098i'],
            'ams': ['dm 2-20', 'dmx', 'dmx15-80', 'rmx 16'],
            'ams neve': ['1073opx', '1073opx', '1081', '33115', '33609/j', 
                         '88rs sp2', 'montserrat'],
            'antelope': ['orion 32+'],
            'anthony demaria labs': ['1000'],
            'aphex': ['104', '662'],
            'api': [ '2500', '312', '3124+', '512c', '529', '550a', 
                    '550b', '560', '525', '1608','lunchbox'],
            'aston': ['stealth', 'spirit'],
            'atc': ['scm25a', 'scm50'],
            'audio technica': ['4033','4050','2040','at4033', 'at4050', 'at2040', 'atm31'],
            'audix': ['om-6', 'd1','d6'],
            'auratone': ['5c super sound', 'c5'],
            'avalon': ['m2', 'm5','vt-737sp', 'ad2022', 'vt-747sp', 'ad2044'],
            'avantone': ['mixcubes', 'cv-12','cla200'],
            'b&k': ['4006','801 d4', '805 d3', '805 d4', '805 matrix', 'db1d', 'htm 1','800 d3'],
            'barefoot sound': ['mm27', 'footprint01', 'micro-main27'],
            'bbe': ['862 sonic maximizer','sonic maximizer 822'],
            'bel electronics': ['bde 2400','bf-20'],
            'bel': ['bde 2400','bf-20'],
            'behringer': ['snr2000'],
            'beyer': ['m500', 'm160', 'm201tg'],
            'beyerdynamic': ['m500', 'm160', 'm-201', 'm-69', 'm-88', 'm-201tg'],
            'black lion audio': ['revolution'],
            'blue': ['reactor ldc'],
            'brauner': ['vm 1'],
            'brent averill': ['1073'],
            'bricasti design': ['m7', 'm10'],
            'bruel & kjaer (dpa)': ['4003', '4006', '4006 (tlx)',
                                    '4007', '4011', '4015', '4061'],
            'bss': ['dpr-402'],
            'burl': ['b2 bomber adc', 'b80 mothership'],
            'cad': ['trion'],
            'calrec': ['cm1050c', 'cm4050'],
            'cartec': ['pre-q5'],
            'cascade': ['fathead', 'fathead ii lundahl', '731r', 'dr2', 'dr2s', 'x15'],
            'cathedral pipes': ['regensburg dom'],
            'charteroak': ['s700'],
            'chandler': ['tg2', 'curve bender', 'rs124', 'tg-1','tg2-500','summing mixer','660',
                         'germ compressor', 'redd.47', 'germanium','redd', 'tg', 'tg l', 'tg eq'],
            'coastal acoustics': ['boxer t5', '5'],
            'coles': ['4038'],
            'conor audio': ['1107'],
            'core sound': ['octo'],
            'cortado': ['mkiii'],
            'cranborne audio': ['camden 500'],
            'crown': ['pzm','pzm-30 gpb','sass-p mkii'],
            'daking': ['52270', '91579'],
            'dangerous music': ['monitor st', 'bax eq', 'convert-2'],
            'dbx': ['120a','120xp ', '160vu', '160xt', '160a', '165a',
                    '160x', '160xt','166a','760x', '902', '903', '904'],
            'deltalab': ['effectron ii'],
            'drawmer': ['1960', 'ds-201', '201','ds201', 'm500', 
                        'vacuum tube 1960 compressors'],
            'dpa': ['4011', '4006', '2011c'],
            'dytronics': ['cyclosonic'],
            'earthworks': ['dx7 dm20', 'dx7 sr25', 'pm40', 'qtc 40mp'],
            'echoplex': ['ep3'],
            'electro-voice': ['ev 1777', 're-15', 're-16', 're-18', 're-20', 
                              're-55', 're320', 'pl20', 're2000', '408', '641'],
            'emi': ['(ribbon) rm1b', 'redd.17', 'tg 12412', 'tg 12413', 'tg 12416r', 'tg12345 mkii'],
            'emotiva': ['stealth 6','stealth 8','pro stealth 6','pro stealth 8'],
            'empirical labs': ['distressor', 'el8 distressors', 
                               'fatso jr', 'derresser'],
            'emt': ['140','240','250','445'],
            'event electronics': ['studios precisions'],
            'eventide': ['h3000', 'h9', 'h8000fw', 'h3500','harmonizer model h949',
                         'dsp4000', 'h9000', 'omnipressor', 'h910','clockworks model h910',
                         'clockworks instant phaser'],
            'fairchild': ['670', '660', '663'],
            'federal': ['am864/u'],
            'fender': ['fr1000'],
            'flea': ['47', '12', '49'],
            'focal': ['twin 6 be', 'sm9', 'trio11 be', 'shape 65','shape'],
            'focusrite': ['isa 110', 'red 3', 'red 8pre','scarlett 18i20', 'isa 828', 
                          '315', '215','isa 215', 'platinum voicemaster'],
            'funkberater': ['md30'],
            'gefel': ['um-92.1s','mv102','um705'],
            'geffell': ['um-92.1s','mv102','um705'],
            'genelec': ['8351a', '1031a', '1032','1032a', '8260a', '8030c'],
            'grace design': ['m101', 'm905'],
            'groove tubes': ['the glory comp'],
            'gml': ['8200', '8304', '8300'],
            'hairball audio': ['lola'],
            'hedd': ['type 20', 'type 30'],
            'Heil': ['pr-20','pr-20'],
            'inovonics': ['model 201'],
            'jbl': ['4401','lsr28p','lsr6823p'],
            'josephson': ['c700a', 'e22s', 'c42'],
            'kii': ['three'],
            'klark technik': ['dn27'],
            'korg': ['a3'],
            'krk': ['rokit 5', 'rokit 8', 'v8','7000b', '9000', 'e8', 'rok bottom sub'],
            'ksm': ['353'],
            'lang': ['peq-2'],
            'lauten': ['ls-308'],
            'lee jackson': ['big iron'],
            'lewitt': ['lct 640 ts', 'lct 1040', 'pure tube'],
            'lexicon': ['200', '224x','300','480l','224xl','960l', 'lxp-1',
                        'lxp-5','pcm42','pcm70','pcm80','pcm91','prime time'],
            'm&k': ['mps-2510'],
            'mackie': ['hr624','hr824'],
            'maestro': ['echoplex ep-3'],
            'manley': ['vari-mu', 'massive passive', 'gold reference',
                       'core', 'reference cardioid', 'vox box', 'pultec','enhanced pultec eqp-1a'],
            'mäag audio': ['eq4', 'preq2'],
            'marshall': ['5002 “a”'],
            'mark-o-matic': ['mpag-d','c-12'],
            'mercenary': ['km69'],
            'micmix': ['master room mr-ii'],
            'microtech gefell': ['m70','m900','m71'],
            'millennia media': ['4-Channel Preamp'],
            'mojave': ['ma 300'],
            'mutronics': ['mutator'],
            'mxr': ['ø1'],
            'neumann': ['582','km53','km 54','km 56','km 64','km83','km84','km86','km84i',
                        'km130','km140','km184','m 49','m 50','m147','m 250','m 269',
                        'mk221','tlm103','tlm50','tlm127','mv102','sm 2','tlm170', 
                        'u47','u57','u67','u87','u87i','u 89 ai','um705'],
            'neve': ['88rlb','88rs sp2','1073','1073opx','1084','1081','2254','33115',
                     '33609','33609/j','33609/c','34628','5052','582','2264x','portico 5024',
                     '9098i','vr60 legend','monserrat'],
            'ns-10': ['subkick'],
            'oktava': ['mk-219', 'ml-52'],
            'osm': ['os800'],
            'otari': ['mtr 10'],
            'pcm': ['81', '91'],
            'pearlman': ['tm-1', 'churcho mic'],
            'peavey': ['Univerb'],
            'presonus': ['studio 24c', 'eureka channel strip'],
            'prism': ['maselec series mla-2'],
            'proac studio': ['100'],
            'pultec': ['eqp-1a', 'meq-5', 'peq-2','hlf-3c'],
            'quantec': ['qrs/l'],
            'quested': ['hq210', 'vh3208'],
            'radial engineering': ['jdi', 'j48', 'pro48', 'd2', 'jdx'],
            'rca': ['ba-6a', '(ribbon) 3043', '(ribbon) bx-44', '(ribbon) dx-77'],
            'ridge farm': ['gas cooker'],
            'rme': ['babyface pro', 'fireface ufx', 'adi-2 pro'],
            'rode': ['nt1','nt2-a','nt1-a','nt-2'],
            'roger mayer': ['456'],
            'roland': ['re-501','chorus echo re-501','dc-30','e-660',
                       'sde 2500','sde 330','sde 3000','sph 323',
                       'srv 330','dimension d', 'gp-8 ', 're 201', 'rsp 550'],
            'rode': ['nt1', 'nt2-a', 'nt-2', 'nt1-a'],
            'roswell audio': ['k47'],
            'royer': ['121','122','r-121', 'r-122', 'r-122 mkII', 'sf-12', 'r10', 'sf-24'],
            'rupert neve designs': ['portico', 'portico ii', '5033', '5211', '5088'],
            'sanken': ['cms 2', 'cu 41'],
            'sansamp tech': ['21 nyc'],
            'schoeps': ['cmc6', 'mk41','cmt 54', 'cmt 540', 'cmt 541', 'cmts 501 u', 
                        'ka 40', 'mk 2', 'mk 21', 'mk 2h', 'mk 2s', 'mk 4', 
                        'mk 41', 'mk 5', 'mk 6', 'mstc5'],
            'se': ['4400a','rnr1','z5600'],
            'sebatron': ['vmp quad plus'],
            'sennheiser': ['421','441','ambeo vr','e609','e904','e906','gooseneck',
                           'md409 u3','md421','md421-n','md421-u','md441','mkh20',
                           'mkh40','mkh105','mkh404','mkh405','mkh416'],
            'shadow hills': ['gama', 'mastering compressor', 'mono gama'],
            'sherman': ['filterbank'],
            'shure': ['55sh', '510', '520dx', '545sd','beta 52a','beta 52','beta 57','beta 57a', 
                      'beta 578a','beta 98amp','ksm32','ksm44','ksm141','sm7','sm7b','sm54',
                      'sm56','sm57','sm58','sm81','sm91 pzm','super 55'],
            'sintefex': ['fx8000'],
            'smart research': ['c1', 'c2'],
            'sontec': ['mes-432c'],
            'sontronics': ['apollo', 'apollo 2', 'aria', 'corona', 'delta', 'delta 2', 
                           'dm-1b', 'halo', 'helios','mercury', 'omega','orpheus', 
                           'saturn', 'sigma', 'sigma 2','stc-1'],
            'sony': ['a7 dat','c800g', 'c37a','c 37p', 'c 38', 'ecm 150', 'emc 22p'],
            'spectrasonics': ['610'],
            'spl': ['transient designer','transient designer 4'],
            'ssl': ['g bus compressor', 'superanalogue','bus', 'bus +',
                    '4000', '9000j', 'fusion', '4056 g+','fx g384'],
            'stager': ['sr-2n'],
            'stc/coles': ['4021 e', '4032 e', '4033', '4038', 'stereo pair & bar'],
            'sterling': ['st31'],
            'summit': ['tpa-200','eqp-200','dcl-200', 'tpa-200a', ' 2290'],
            'summit audio': ['tpa-200','eqp-200','dcl-200', 'tpa-200a', ' 2290'],
            't.c. electronic': ['fireworx','m2000','m3000','m5000','2290', 'system 6000', 'tc 1128'],
            'tc electronic': ['fireworx','m2000','m3000','m5000','2290', 'system 6000', 'tc 1128'],
            'tab funkenwerk': ['u67'],
            'tannoy': ['little gold monitors'],
            'teegarden audio': ['ppc-125'],
            'telefunken': ['ela m 251', 'u47', 'ak47','cu-29 copperhead', 
                           'tf39', 'u48','m 81', 'm12f'],
            'teletronix': ['la2a','la-2a'],
            'tl audio': ['eq-2 parametric', 'pp 10', 'tla n1'],
            'thermionic culture': ['phoenix', 'fat bustard', 
                                   'vulture', 'earlybird', 'pullet'],
            'tree audio': ['branch ii'],
            'trident': ['88'],
            'tube-tech': ['cl1b', 'pe-1c', 'pe-1b','cl 1a', 'cl 1b', 'lca 2b'],
            'universal audio': ['1176','1176ln', '610','la-2a','la-610 mk ii', '2-610','dbx 160','dbx 160a'],
            'urei': ['545','1176','1175b','1176 ln','1178','1178ln','la-10','la-4'],
            'valley people': ['dyna-mite'],
            'vintech audio': ['x-81', 'x73i'],
            'vintech': ['x-81', 'x73i'],
            'vitavox': ['b 50'],
            'ward beck': ['M441'],
            'warm': ['76','251','414','412','8000', 'bus comp','eqp wa','u47','u67','u87',
                     'wa14','wa2a','wa44','wa412','wa73','wa76','wa87'],
            'warm audio': ['76','251','414','412','8000', 'bus comp','eqp wa','u47','u67','u87',
                     'wa14','wa2a','wa44','wa412','wa73','wa76','wa87'],
            'wem': ['Copicat'],
            'yamaha': ['ns10m', 'hs8', 'spx90', 'spx90ii','spx1000s','rev7', 'pro r3', 'yst-sw200']
        }
  
        self.equipment = set()
        for manufacturer, models in self.equipment_hierarchy.items():
            # Add full names (manufacturer + model)
            self.equipment.update(f"{manufacturer} {model}" for model in models)
            # Add model numbers alone
            self.equipment.update(models)

        # Terms that should score higher when used as headers or links
        self.header_boost_terms = {
            'equipment list': 3.0, 'gear list': 3.0, 'microphone list': 2.5,
            'equipment': 2.0, 'gear': 2.0, 'outboard': 2.0, 'tech specs': 2.0,
            'specifications': 1.5, 'studio specs': 1.5, 'microphones': 1.0, 'valve': 1.0,
            'tube': 1.0, 'condensers': 1.5, 'ribbon': 1.0, 'hardware': 1.0, 'monitors': 1.0, 
            'compressors': 0.5, 'preamps': 0.5, 'equalisers': 0.5, 'equalizers': 0.5,
            'processors': 0.4, 'plugins': 0.2, 
        }

        
        self.url_score_weights = {
            # High priority terms
            'equipment list': 20.0, 'gear list': 20.0, 'microphone list': 20.0, 'mic list': 20.0,
            # Medium-high priority terms
            'gear': 10.0, 'equipment': 10.0, 'inventory': 10.0, 'microphones': 8.0, 'tech spec': 9.0,
            'studio': 8.5, 'studios': 8.5, 'microphone': 7.0,
            # Medium priority terms
            'specs': 6.5, 'spec': 6.5, 'technik': 6.5,'studo': 6.0,'instruments': 5.0, 
            # Lower priority terms
            'list': 4.0,
            'console': 0.7, 'monitors': 0.7, 'desk': 0.7, 'mic locker': 0.7,
            'monitoring': 0.6, 'speakers': 0.6, 'outboard': 0.6, 'hardware': 0.6, 'backline': 0.6,
            'compressors': 0.5, 'preamps': 0.5, 'equalisers': 0.5, 'equalizers': 0.5,
            'processors': 0.4,
            'live room': 0.3, 'tracking': 0.3, 'control room': 0.3,
            'tech': 0.3, 'condensers': 0.3, 'tube': 0.3, 'ribbon': 0.3, 'valve': 0.3,
            'setup': 0.2, 'isolation booth': 0.1, 'services': 0.05,
            'facilities': 0.01, 'recording': 0.01,
            'tour': -3.0
        }

        # Terms to ignore/skip
        self.ignore_terms = {
            'clients', 'blog', 'contact', 'location', 'meet', 'team', 'staff', 'music', 'techniques',
            'news', 'rates', 'calendar', 'experience', 'restaurant', 'hotel', 'sleep', 'content', 
            'cafe', 'shop', 'gallery', 'merch', 'merchandise', 'past', 'previous', 'demo', 'package',
            'work', 'cart', 'artists', 'acts', 'bands', 'policies', 'conditions', 'listen','quote', 
            'sounds', 'accommodation', 'links', 'photos', 'records', 'event', 'events','community',
            'visit', 'online', 'learn', 'teach', 'study', 'institute', 'mastering', 'archive', 
            'filming', 'streaming', 'story', 'press', 'talk', 'newsletter', 'chatting', 'chat', 
            'jobs', 'careers', 'film', 'engineers', 'history', 'guests', 'guest book', 'label',
            'publishing', 'management', 'resident', 'residential', 'covid', 'book', 'booking', 
            'mailto:', 'tel:', 'virtual', 'project', 'food', 'drink', 'snacks', 'lounge', 
            'workshop', 'program', 'school', 'login', 'retreat', 'producer', 'floor plan', 
            'photography', 'privacy', 'policy', 'touch', 'party', 'parties', 'sitemap','art',
            'tips', 'advice', 'expert', 'singer', 'songwriter', 'writing', 'songwriting','payment',
            'cinema', 'visual', 'entertainment', 'preparing', 'prepare', 'pricing', '.jpg',
            'voice','voice over','discography', 'samples','radio','affiliation','sponsor', 'virual',
            'tab','tabs','searchbox','widget','subtitling'
        }

        # Content scoring weights
        self.content_score_weights = {
            'instruments': 0.5, 'microphone': 0.5, 'console': 0.5, 'monitors': 1.5, 'desk': 1.5, 
            'compressors': 1.5, 'equalisers': 1.5, 'equalizers': 1.5, 
            'processors': 0.5, 'outboard': 1.0,
            'condensers': 1.0, 'tube': 1.0, 'ribbon': 1.0, 'preamps': 1.2, 'valve': 1.0,
            'backline': 1.0, 'plugins': 0.5, 'converters': 0.5, 'daws': 0.5, 'plug ins': 0.5,
            'synths': 0.3, 'guitars': 0.2, 'electric piano': 0.3, 'electric keyboards': 0.3,
            'electric organ': 0.3, 'pedals': 0.3
        }

        # Equipment and manufacturer scoring weights
        self.equipment_score = 6.5
        self.manufacturer_score = 2.5
        
        # Configure requests session
        self.session = self._setup_requests_session()
        
        # Configure Selenium if enabled
        if self.use_selenium:
            self.driver = self._setup_selenium_driver()
        
        # Proxy configuration
        self.proxies = []
    
    def _setup_requests_session(self):
        """Configure requests session with proper connection pooling."""
        session = requests.Session()
        # Create separate connection pools for different domains
        adapter = HTTPAdapter(
            pool_connections=25,
            pool_maxsize=25,
            pool_block=False,  # Don't block when pool is full
            max_retries=Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[500, 502, 503, 504]
            )
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def _setup_selenium_driver(self):
        """Configure Selenium WebDriver with appropriate options."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--page-load-strategy=eager')  # Don't wait for all resources

        # Create driver with custom timeout settings
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)  # Reduce from default 300 seconds
        driver.set_script_timeout(30)

        return driver
    
    def cleanup(self):
        """Clean up resources."""
        if self.use_selenium:
            self.driver.quit()  

#### Main Processing Pipeline ####

    def scrape_studios(self, input_file: str, output_file: str, detailed_output_file: str):
        """Main method to process all studios from CSV."""
        # Read input CSV
        df = pd.read_csv(input_file)
        studios = df.to_dict('records')
        
        # Process in batches
        all_results = []
        for i in range(0, len(studios), self.batch_size):
            batch = studios[i:i + self.batch_size]
            batch_results = self.process_batch(batch)
            all_results.extend(batch_results)
            
            # Progress tracking
            logger.info(f"Processed {min(i + self.batch_size, len(studios))}/{len(studios)} studios")
        
        # Save basic results
        pd.DataFrame(all_results).to_csv(output_file, index=False)
        
        # Save detailed results
        detailed_results = [
            {
                'studio_name': r['studio_name'],
                'equipment_page_url': r['equipment_page_url'],
                'confidence_score': r['confidence_score'],
                'context': r['context']
            }
            for r in all_results
            if r['equipment_page_url']  # Only include studios with found equipment pages
        ]
        pd.DataFrame(detailed_results).to_csv(detailed_output_file, index=False)
    
    def process_batch(self, studios: List[Dict]) -> List[Dict]:
        """Process a batch of studios using parallel execution."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_studio = {
                executor.submit(
                    self.scrape_studio,
                    studio['studio_name'],
                    studio['website']
                ): studio
                for studio in studios
            }
            
            results = []
            for future in as_completed(future_to_studio):
                results.append(future.result())
        
        return results
    
    def scrape_studio(self, studio_name: str, website: str) -> Dict:
        result = {
            'studio_name': studio_name,
            'website': website,
            'status': 'Inactive',
            'error_message': '',
            'equipment_page_url': '',
            'download_link': '',
            'confidence_score': 0.0,
            'context': '',
            'structured_content': []
        }

        equipment_pages = set()
        pages_checked = 0

        try:
            try:
                self.driver.current_url
            except:
                logger.warning("WebDriver seems unresponsive, resetting...")
                self.driver.quit()
                self.driver = self._setup_selenium_driver()
            
            pages_to_check = [(website, 0.0)]
            base_domain = urlparse(website).netloc
            visited_urls = set()

            while pages_to_check and pages_checked < self.max_pages_per_studio:
                current_url, base_score = pages_to_check.pop(0)

                # Skip if already visited
                if current_url in visited_urls:
                    continue

                # First check if URL should be ignored
                url_lower = current_url.lower()
                if any(term in url_lower for term in self.ignore_terms):
                    continue

                # Calculate URL score before making request
                url_score = self.calculate_url_score(current_url)
                if url_score < 0:  # Skip if negative score
                    continue

                visited_urls.add(current_url)
                pages_checked += 1

                try:
                    if self.use_selenium:
                        page_content = self.scrape_with_selenium(current_url)
                    else:
                        response = self.session.get(current_url, timeout=30, verify=self.verify_ssl)
                        page_content = response.text

                    soup = BeautifulSoup(page_content, 'html.parser')
                    result['status'] = 'Active'

                    # Calculate total page score
                    page_score = url_score  # Start with URL score
                    structured_content = self.extract_structured_content(soup)
                    download_links = self.extract_download_links(soup, current_url)

                    # Add content-based scoring
                    if structured_content:
                        page_score += self.calculate_content_score(structured_content)
                    if download_links:
                        page_score += 0.2
                        result['download_link'] = '; '.join(download_links)

                    # Only add pages with positive scores
                    if page_score > 0:
                        equipment_pages.add((current_url, page_score))
                        self.url_scores[current_url] = page_score

                    # Only process new internal links if we haven't hit our limit
                    if pages_checked < self.max_pages_per_studio:
                        for link in soup.find_all('a'):
                            href = link.get('href')
                            if href:
                                full_url = urljoin(current_url, href)
                                parsed_url = urlparse(full_url)
                                if (parsed_url.netloc == base_domain and 
                                    full_url not in visited_urls and
                                    not any(term in full_url.lower() for term in self.ignore_terms)):
                                    pages_to_check.append((full_url, 0.0))

                except Exception as e:
                    logger.warning(f"Error processing {current_url}: {str(e)}")
                    continue

            if equipment_pages:
                # Sort by score and filter out pages below threshold
                sorted_pages = sorted(equipment_pages, key=lambda x: x[1], reverse=True)
                filtered_pages = [(url, score) for url, score in sorted_pages if score >= 290]

                if filtered_pages:
                    result['equipment_page_url'] = '; '.join(
                        f"{url} ({score:.2f})" for url, score in filtered_pages
                    )
                    result['confidence_score'] = max(score for _, score in filtered_pages)
                else:
                    # If no pages meet the threshold, leave equipment_page_url empty
                    result['equipment_page_url'] = ''
                    result['confidence_score'] = max(score for _, score in sorted_pages) if sorted_pages else 0.0

            return result

        except Exception as e:
            result['status'] = 'Inactive'
            result['error_message'] = str(e)
            return result

#### URL and Content Processing ####
        
    def calculate_url_score(self, url: str) -> float:
        """Calculate URL score using only the highest scoring term found."""
        # Handle URL fragments
        url = url.split('#')[0]  # Remove fragment before processing

        url_lower = url.lower()
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')

        # Early exit for ignored terms
        if any(term in url_lower for term in self.ignore_terms):
            return -1.0

        score = 0.0
        highest_term_score = 0.0

        # Check navigation elements for header boost terms
        if path_parts:
            nav_element = path_parts[-1].lower() if path_parts[-1] else (
                path_parts[-2].lower() if len(path_parts) > 1 else '')

            # Header boost terms are still all counted as they indicate structure
            for term, boost in self.header_boost_terms.items():
                if term.replace(' ', '-') in nav_element or term.replace(' ', '') in nav_element:
                    score += boost

        # Find highest scoring term from url_score_weights
        for term, weight in self.url_score_weights.items():
            if term in url_lower:
                highest_term_score = max(highest_term_score, weight)

        # Add only the highest term score to the total
        score += highest_term_score

        return score
    
    def calculate_content_score(self, structured_content: List[Dict]) -> float:
        """Calculate score based on structured content with improved equipment detection."""
        score = 0.0
        term_counts = {}
        equipment_counts = {}
        manufacturer_counts = {}

        for section in structured_content:
            header_text = self.normalize_text(section['header'])
            content_text = self.normalize_text(' '.join(section['content']))

            # Header boost terms remain unchanged
            for term, boost in self.header_boost_terms.items():
                if term in header_text:
                    score += boost

            # Content type scoring remains unchanged
            if section['type'] == 'list' and len(section['content']) > 3:
                score += 0.5
            elif section['type'] == 'table' and len(section['content']) > 3:
                score += 0.75

            # Enhanced equipment detection
            for manufacturer, models in self.equipment_hierarchy.items():
                normalized_manufacturer = self.normalize_text(manufacturer)

                # Check manufacturer presence
                if normalized_manufacturer in header_text or normalized_manufacturer in content_text:
                    manufacturer_counts[manufacturer] = manufacturer_counts.get(manufacturer, 0) + 1
                    if manufacturer_counts[manufacturer] <= 6:
                        score += self.manufacturer_score

                # Check each model with variations
                for model in models:
                    variations = self.generate_equipment_variations(manufacturer, model)
                    equipment_key = f"{manufacturer} {model}"

                    # Check if any variation matches
                    if not equipment_counts.get(equipment_key):
                        for variation in variations:
                            if variation in content_text:
                                equipment_counts[equipment_key] = True
                                score += self.equipment_score
                                break

            # Content terms (counted once)
            for term, weight in self.content_score_weights.items():
                if term not in term_counts and term in content_text:
                    term_counts[term] = True
                    score += weight

        return score

    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def normalize_text(self, text: str) -> str:
        """Enhanced text normalization to handle various formats."""
        text = text.lower()
        text = re.sub(r'[/\\_-]', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def generate_equipment_variations(self, manufacturer: str, model: str) -> Set[str]:
        """Generate common variations of equipment names."""
        variations = set()

        # Normalize manufacturer and model
        manufacturer = self.normalize_text(manufacturer)
        model = self.normalize_text(model)

        # Add full name variations
        variations.add(f"{manufacturer} {model}")
        variations.add(f"{manufacturer}{model}")
        variations.add(model)  # Model number alone

        # Handle number-only models
        if model.isdigit():
            variations.add(f"model {model}")
            variations.add(f"type {model}")

        return variations

#### Content Extraction Methods ####

    def extract_structured_content(self, soup: BeautifulSoup) -> List[Dict]:
        """Enhanced extraction of structured content, handling lists, tables, and standalone content."""
        structured_content = []

        # First process header-based sections as in original code
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        processed_elements = set()  # Track elements we've processed

        for header in headers:
            header_text = header.get_text().strip()

            section = {
                'header': header_text,
                'content': [],
                'type': 'text'  # Default type
            }

            current = header.find_next_sibling()
            while current and current.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                processed_elements.add(current)

                if current.name in ['ul', 'ol']:
                    section['type'] = 'list'
                    for item in current.find_all('li'):
                        section['content'].append(item.get_text().strip())
                        processed_elements.add(item)

                elif current.name == 'table':
                    section['type'] = 'table'
                    for row in current.find_all('tr'):
                        cells = row.find_all(['td', 'th'])
                        if cells:
                            row_content = ' | '.join(cell.get_text().strip() for cell in cells)
                            section['content'].append(row_content)
                        processed_elements.add(row)

                elif current.name == 'div':
                    # Check for table-like divs (grid layouts)
                    if 'table' in current.get('class', []) or 'grid' in current.get('class', []):
                        section['type'] = 'table'
                        items = current.find_all(['div', 'span'])
                        for item in items:
                            text = item.get_text().strip()
                            if text:
                                section['content'].append(text)
                                processed_elements.add(item)

                    # Check for list-like divs
                    elif any(cls in current.get('class', []) for cls in ['list', 'items']):
                        section['type'] = 'list'
                        items = current.find_all(['div', 'span'])
                        for item in items:
                            text = item.get_text().strip()
                            if text:
                                section['content'].append(text)
                                processed_elements.add(item)

                elif current.name == 'p':
                    if section['type'] == 'text':  # Only add if we haven't found a list/table yet
                        section['content'].append(current.get_text().strip())

                current = current.find_next_sibling()

            # Only add sections with meaningful content
            if len(section['content']) > 0:
                structured_content.append(section)

        # Now process standalone content that wasn't part of any header section
        standalone_content = []
        for element in soup.find_all(['p', 'div', 'ul', 'ol', 'table']):
            # Skip if we've already processed this element
            if element in processed_elements:
                continue

            content_text = element.get_text().strip()
            if not content_text:
                continue

            if element.name in ['ul', 'ol']:
                section = {
                    'header': '',
                    'content': [item.get_text().strip() for item in element.find_all('li')],
                    'type': 'list'
                }
            elif element.name == 'table':
                section = {
                    'header': '',
                    'content': [],
                    'type': 'table'
                }
                for row in element.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_content = ' | '.join(cell.get_text().strip() for cell in cells)
                        section['content'].append(row_content)
            elif element.name == 'div':
                # Only process divs that look like they contain equipment info
                text_content = element.get_text().strip().lower()
                if any(keyword in text_content for keyword in self.url_keywords):
                    section = {
                        'header': '',
                        'content': [content_text],
                        'type': 'text'
                    }
                else:
                    continue
            else:  # paragraphs
                section = {
                    'header': '',
                    'content': [content_text],
                    'type': 'text'
                }

            if section['content']:
                standalone_content.append(section)

        # Combine all content, putting header-based sections first
        structured_content.extend(standalone_content)

        return structured_content
    
    def extract_download_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract equipment-specific download links with enhanced detection for interactive elements."""
        download_links = []

        # Enhanced selectors for download elements
        download_selectors = {
            'links': [
                'a[href*=".pdf"]',
                'a[href*="download"]',
                'a[href*="equipment"]',
                'a[class*="download"]',
                'a[class*="btn"]',
                '.download a',
                '.btn-download',
                '[data-link*="tech-equip"]',  # Abbey Road specific
                '[data-link*="equipment"]'
            ],
            'containers': [
                '.download',
                '.equipment-list',
                '.tech-specs',
                '.specifications',
                '[id*="tech"]',
                '[class*="tech"]',
                '.detail'  # Abbey Road specific
            ]
        }

        # First check direct download links
        for selector in download_selectors['links']:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href', '')
                data_link = element.get('data-link', '')

                # Handle both regular links and data-link attributes
                if href:
                    full_url = urljoin(base_url, href)
                elif data_link:
                    full_url = urljoin(base_url, data_link)
                else:
                    continue

                if self._is_valid_download_link(full_url, element):
                    download_links.append(full_url)

        # Then check container elements that might have nested download links
        for selector in download_selectors['containers']:
            containers = soup.select(selector)
            for container in containers:
                # Look for download links within containers
                for link in container.find_all('a'):
                    href = link.get('href', '')
                    if href:
                        full_url = urljoin(base_url, href)
                        if self._is_valid_download_link(full_url, link):
                            download_links.append(full_url)

        # Remove duplicates while preserving order
        return list(dict.fromkeys(download_links))

    def _is_valid_download_link(self, url: str, element) -> bool:
        """Helper method to validate download links with enhanced checks."""
        url_lower = url.lower()

        # Get all relevant text
        element_text = element.get_text().strip().lower()
        title_text = element.get('title', '').lower()
        aria_label = element.get('aria-label', '').lower()

        # Get parent context
        parent = element.find_parent()
        parent_text = parent.get_text().strip().lower() if parent else ''
        parent_class = ' '.join(parent.get('class', [])).lower() if parent else ''

        # Combine all text for checking
        all_text = f"{element_text} {title_text} {aria_label} {parent_text} {url_lower}"

        # Skip unwanted content
        if any(term in all_text for term in ['floor plan', 'directions', 'contact']):
            return False

        # Check file extensions
        valid_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv'}
        if any(url_lower.endswith(ext) for ext in valid_extensions):
            return True

        # Check for download indicators
        download_indicators = {
            'download', 'equipment', 'spec', 'technical', 'gear list',
            'mic list', 'specifications', 'tech sheet'
        }

        # Check if parent has download-related classes
        if 'download' in parent_class or 'btn' in parent_class:
            return True

        # Check if any download indicators are present in text
        return any(indicator in all_text for indicator in download_indicators)

    def extract_content_from_pdf(self, pdf_url: str) -> str:
        """Download and extract text content from PDF."""
        try:
            response = self.session.get(pdf_url, timeout=30)
            pdf_content = io.BytesIO(response.content)
            
            reader = PdfReader(pdf_content)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            logger.warning(f"Error extracting PDF content from {pdf_url}: {str(e)}")
            return ""

    def scrape_with_selenium(self, url: str) -> str:
        """Scrape page content using Selenium with improved JavaScript handling 
                        and interactive element detection."""
        try:
            self.driver.get(url)

            # Initial wait for page load
            time.sleep(3)

            # First find and click any collapsible sections/accordions
            collapsible_selectors = [
                "[data-toggle='collapse']",  # Bootstrap collapse
                ".collapsible",             # Common class name
                ".accordion-button",        # Bootstrap accordion
                ".expandable",             # Generic expandable
                "[aria-expanded]",         # ARIA attribute
                ".toggle-content",         # Common toggle class
                "[role='button']",         # ARIA role button
                ".item[data-link]"         # Abbey Road specific
            ]

            for selector in collapsible_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            # Check if element is visible and clickable
                            if element.is_displayed():
                                # Scroll element into view
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(0.5)  # Brief pause for scroll

                                # Try regular click first
                                try:
                                    element.click()
                                except ElementClickInterceptedException:
                                    # If regular click fails, try JavaScript click
                                    self.driver.execute_script("arguments[0].click();", element)

                                # Wait for potential animations
                                time.sleep(1)

                                # If element has data-link attribute (Abbey Road specific)
                                data_link = element.get_attribute('data-link')
                                if data_link:
                                    # Construct full URL if needed
                                    if data_link.startswith('/'):
                                        parsed_url = urlparse(url)
                                        modal_url = f"{parsed_url.scheme}://{parsed_url.netloc}{data_link}"
                                        # Load modal content
                                        self.driver.get(modal_url)
                                        time.sleep(1)
                                        # Go back to main page
                                        self.driver.back()
                                        time.sleep(1)

                        except Exception as e:
                            logger.debug(f"Error interacting with element: {str(e)}")
                            continue

                except Exception as e:
                    logger.debug(f"Error finding elements with selector {selector}: {str(e)}")
                    continue

            # Scroll through the page to trigger lazy loading
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down in smaller increments
                for i in range(0, last_height, 300):
                    self.driver.execute_script(f"window.scrollTo(0, {i});")
                    time.sleep(0.2)

                # Calculate new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Wait for any final dynamic content
            time.sleep(2)

            return self.driver.page_source

        except Exception as e:
            logger.warning(f"Error using Selenium for {url}: {str(e)}")
            return ""
        
# Usage example:
if __name__ == "__main__":
    scraper = StudioEquipmentScraper(
        max_workers=1,
        rate_limit_delay=3.5,
        batch_size=10,
        verify_ssl=True,
        use_selenium=True
    )
    
    try:
        scraper.scrape_studios(
            input_file='studio_websites_ix.csv',
            output_file='studio_equip_lists/equip_search_sel_ix2.csv',
            detailed_output_file='studio_equip_lists/detailed_equip_sel_ix2.csv'
        )
    finally:
        scraper.cleanup()