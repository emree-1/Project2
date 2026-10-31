from playwright.sync_api import sync_playwright
import json, os
from pathlib import Path
from tempfile import mkdtemp
ARTIFACTS = Path(mkdtemp(prefix="ckb-tests-"))
ROOT = Path(__file__).resolve().parents[1]
import threading, http.server, functools
server=http.server.ThreadingHTTPServer(("127.0.0.1",8765),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000});errors=[];requests=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
 page.goto('http://127.0.0.1:8765/cybersecurity-knowledge-base.html');page.wait_for_selector('h1');print('TITLE',page.locator('h1').inner_text());print('ERRORS',errors)
 results=page.evaluate('CKBDiagnostics.run()');print(json.dumps(results,ensure_ascii=False,indent=2));assert all(t['pass'] for t in results)
 page.get_by_role('button',name='Architecture & cas d’usage',exact=True).click()
 page.get_by_text('API REST',exact=True).check();print('TABLE ROWS',page.locator('tbody tr').count());assert page.locator('tbody tr').count()>0
 page.get_by_text('Base SQL',exact=True).check()
 page.get_by_label('Source du flux',exact=True).select_option(label='API REST')
 page.get_by_label('Destination du flux',exact=True).select_option(label='Base SQL')
 page.get_by_label('Protocole du flux',exact=True).fill('TLS')
 page.get_by_role('button',name='Ajouter le flux',exact=True).click()
 page.get_by_role('button',name='Enregistrer l’évaluation',exact=True).click();assert page.evaluate('CKBDiagnostics.snapshot().workspaces.length')==1
 assert page.evaluate('CKBDiagnostics.snapshot().workspaces[0].flows[0].protocol')=='TLS'
 page.screenshot(path=str(ARTIFACTS/'screenshot.png'),full_page=False)
 page.get_by_role('button',name='Explorateur de composants',exact=True).click();page.get_by_role('button',name='Nouvel enregistrement',exact=True).click()
 page.get_by_label('Nom',exact=True).fill('Composant test');page.get_by_label('Domaine',exact=True).fill('Tests');page.get_by_role('button',name='Enregistrer',exact=True).click()
 assert page.evaluate("CKBDiagnostics.snapshot().components.some(c=>c.name==='Composant test')")
 page.reload();page.wait_for_selector('h1');assert page.evaluate("CKBDiagnostics.snapshot().components.some(c=>c.name==='Composant test')")
 
 # Export and restore through real file chooser and preview, and reject malicious data atomically.
 with page.expect_download() as dl:
  page.get_by_role('button',name='Exporter la sauvegarde',exact=True).click()
 export_path=dl.value.path()
 payload=json.loads(Path(export_path).read_text())
 assert payload['data']==page.evaluate('CKBDiagnostics.snapshot()')
 page.get_by_role('button',name='Gestion du référentiel',exact=True).click()
 before=page.evaluate('CKBDiagnostics.snapshot()')
 bad=json.loads(json.dumps(payload));bad['data']['sources'][0]['officialUrl']='javascript:alert(1)'
 def upload(payload):
  with page.expect_file_chooser() as fc:
   page.get_by_role('button',name='Importer JSON',exact=True).click()
  fc.value.set_files({'name':'test.json','mimeType':'application/json','buffer':json.dumps(payload).encode()})
 upload(bad)
 page.get_by_role('heading',name='Import refusé',exact=True).wait_for()
 assert before==page.evaluate('CKBDiagnostics.snapshot()')
 page.get_by_role('button',name='Fermer',exact=True).click()
 upload(payload)
 page.get_by_role('heading',name='Prévisualisation avant import',exact=True).wait_for()
 page.get_by_role('button',name='Confirmer l’import',exact=True).click()
 assert before==page.evaluate('CKBDiagnostics.snapshot()')
 # CSV export/import round-trip exercises the real schema and relationship columns.
 page.get_by_role('button',name='Explorateur de composants',exact=True).click()
 csv_before=page.evaluate('CKBDiagnostics.snapshot()')
 with page.expect_download() as csv_download:
  page.get_by_role('button',name='Exporter CSV',exact=True).click()
 csv_path=csv_download.value.path()
 with page.expect_file_chooser() as csv_chooser:
  page.get_by_role('button',name='Importer CSV',exact=True).click()
 csv_chooser.value.set_files({'name':'composants.csv','mimeType':'text/csv','buffer':Path(csv_path).read_bytes()})
 page.get_by_role('heading',name='Prévisualisation avant import',exact=True).wait_for()
 page.get_by_role('button',name='Confirmer l’import',exact=True).click()
 assert csv_before==page.evaluate('CKBDiagnostics.snapshot()')
 page.get_by_role('button',name='Gestion du référentiel',exact=True).click()
 # All ordinary imported text stays inert after committing a valid backup.
 hostile=json.loads(json.dumps(payload));hostile['data']['components'][0]['name']='<img src=x onerror="window.PWNED=1">'
 upload(hostile)
 page.get_by_role('button',name='Confirmer l’import',exact=True).click()
 page.get_by_role('button',name='Explorateur de composants',exact=True).click()
 assert page.locator('#view img').count()==0 and page.evaluate('window.PWNED === undefined')
 # Edit and delete a new component using the normal UI and explicit deletion confirmation.
 page.get_by_role('button',name='Nouvel enregistrement',exact=True).click()
 page.get_by_label('Nom',exact=True).fill('Cycle CRUD')
 page.get_by_role('button',name='Enregistrer',exact=True).click()
 card=page.locator('article').filter(has=page.get_by_role('heading',name='Cycle CRUD',exact=True))
 card.get_by_role('button',name='Ouvrir la fiche →').click()
 page.get_by_role('button',name='Modifier',exact=True).click()
 page.get_by_label('Nom',exact=True).fill('Cycle modifié')
 page.get_by_role('button',name='Enregistrer',exact=True).click()
 page.locator('article').filter(has=page.get_by_role('heading',name='Cycle modifié',exact=True)).get_by_role('button',name='Ouvrir la fiche →').click()
 page.get_by_role('button',name='Supprimer',exact=True).click()
 page.get_by_role('button',name='Confirmer la suppression',exact=True).click()
 assert not page.evaluate("CKBDiagnostics.snapshot().components.some(c=>c.name==='Cycle modifié')")
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
 page.set_viewport_size({'width':1440,'height':1000})
 page.get_by_role('button',name='Architecture & cas d’usage',exact=True).click()
 page.pdf(path=str(ARTIFACTS/'report.pdf'),format='A4')
 print('IMPORT/EXPORT, CRUD, XSS, MOBILE AND PRINT: passed; artifacts:',ARTIFACTS)
 print('NETWORK',requests);print('ERRORS',errors);assert not errors;assert all(u.startswith('http://127.0.0.1:8765/') for u in requests)
 # Storage denied, including fallback, on a fresh browser context.
 ctx=browser.new_context();ctx.add_init_script("Object.defineProperty(window,'indexedDB',{get(){throw Error('denied')}});Object.defineProperty(window,'localStorage',{get(){throw Error('denied')}})")
 q=ctx.new_page();q.goto('http://127.0.0.1:8765/cybersecurity-knowledge-base.html');q.wait_for_selector('h1');assert 'Mode session' in q.locator('#storage').inner_text();print('STORAGE FAILURE: visible warning')
 browser.close()
