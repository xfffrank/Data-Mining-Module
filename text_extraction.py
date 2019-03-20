from bs4 import BeautifulSoup
import os
import time


root_dir = 'gap-html/'
test_file = 'gap-html/gap_WORMAAAAYAAJ/00000008.html'

def extract_page(file):
    page_txt = ''
    with open(file) as f:
        soup = BeautifulSoup(f, 'lxml')
    # page_txt = soup.find('body').get_text(' ', strip=True)
    try:  # Remove the first block because it may disconnect the words.
        soup.find(name='div', class_='ocrx_block').decompose()
    except:   # empty page
        return ''
    lines = soup.find_all(name='span', class_='ocr_line')
    for l in lines:
        temp = l.get_text()
        l_txt = l.get_text().strip().replace('\xad', '')
        # \xad refers to the word that is cut into two parts
        line_break = '' if '\xad' in temp else ' '
        page_txt += l_txt + line_break
    return page_txt

def extract_text(dir):
    text = ''
    for file in sorted(os.listdir(dir), key=lambda s: int(s.split('.')[0])):
        if file.endswith('.html'):
            # print(file)
            file = os.path.join(dir, file)
            # print(file)
            page_txt = extract_page(file)
            # print(page_txt)
            text += page_txt
    return text


def main(root):
    print('start...')
    start = time.time()
    text_dir = 'texts/'
    for f in os.listdir(root_dir):
        sub_dir = os.path.join(root_dir, f)
        if os.path.isdir(sub_dir):
            print('processing:', sub_dir)
            text = extract_text(sub_dir)
            filename = f + '.txt'
            print('saving...')
            with open(text_dir + filename, 'w') as f:
                f.write(text)
    print('Time elapsed: %.2f' % (time.time() - start))
        

def test():
    txt = extract_page(test_file)
    print(txt)

main(root_dir)
# test()
