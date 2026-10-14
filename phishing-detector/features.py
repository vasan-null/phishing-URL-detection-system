import re, math
from urllib.parse import urlparse
import tldextract

KEYWORDS = ['login','verify','update','secure','bank','account','confirm','password']
SHORTENERS = ['bit.ly','tinyurl.com','goo.gl','t.co','ow.ly','is.gd']
BAD_TLDS = ['tk','xyz','top','gq','ml','cf','ga','work','click']

def entropy(s):
    if not s: return 0
    probs = [s.count(c)/len(s) for c in set(s)]
    return -sum(p*math.log2(p) for p in probs)

def extract_features(url):
    p = urlparse(url if '://' in url else 'http://' + url)
    host = p.netloc.split(':')[0]
    ext = tldextract.extract(url)
    return {
        'url_length': len(url),
        'host_length': len(host),
        'num_dots': url.count('.'),
        'num_hyphens': host.count('-'),
        'has_at': int('@' in url),
        'has_ip': int(bool(re.fullmatch(r'\d{1,3}(\.\d{1,3}){3}', host))),
        'num_subdomains': len([s for s in ext.subdomain.split('.') if s]),
        'is_https': int(p.scheme == 'https'),
        'digit_ratio': sum(c.isdigit() for c in url)/max(len(url),1),
        'special_chars': len(re.findall(r'[^\w\.\-/:]', url)),
        'keyword_count': sum(k in url.lower() for k in KEYWORDS),
        'is_shortener': int(host in SHORTENERS),
        'bad_tld': int(ext.suffix.split('.')[-1] in BAD_TLDS),
        'path_depth': len([x for x in p.path.split('/') if x]),
        'num_params': len(p.query.split('&')) if p.query else 0,
        'double_slash': int('//' in p.path),
        'domain_entropy': entropy(ext.domain),
        'has_port': int(p.port is not None),
    }
