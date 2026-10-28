# 世界遺產大全 — 網站建置指令（給子代理）

目標：在 /home/claude/world-heritage-atlas/index.html 寫出單檔靜態網站（無建置步驟，GitHub Pages 直接開），繁體中文介面，與姊妹站同風格。

參考風格（只讀，照抄 CSS 變數、字型、主題切換、頂欄、卡片與燈箱的寫法即可，不要改那些檔）：/home/claude/bible-atlas/index.html、/home/claude/sculpture-atlas/index.html。

## 資料（fetch 'data/xxx.json'，cache:'no-cache'）
- data/sites.json：陣列，每處 {id, en, zh(可能 null→顯示 en), cat: cultural|natural|mixed, criteria:["i",...], year, ext:[擴展年], danger:bool, trans:bool, iso:["JP",...], regions:["asia",...], coord:[lat,lon]|null, unesco:url, q:[Wikidata Q], en_desc, intro(繁中介紹，可能尚無), highlights:[要點]（可能尚無）, photos:[{file, artist, license, license_url, src:"img/800/<id>_<k>.webp", thumb:"img/thumb/<id>_0.webp"(僅第 0 張有)}]（可能空）}
- data/countries.json：[{iso, en, zh, regions, n}]
- data/regions.json：[{id, zh, en}]
- data/meta.json：{version, updated, counts:{sites,cultural,natural,mixed,danger,countries,with_photo,with_intro}, notes:[...]}

## 版面
1. 頂欄：站名「世界遺產大全」＋英文副標 World Heritage Atlas＋統計列；分頁：總覽／地區／國家／類型／年代／瀕危／地圖／搜尋。
2. 總覽：大張隨機精選照片牆（有照片者），點進單頁。
3. 地區：5 大區卡片 → 該區國家清單（國旗用 emoji 區域指示符由 iso 產生）→ 國家頁列出該國遺產卡片（主圖縮圖、中文名、英文名、類型色標、登錄年、瀕危紅標）。
4. 國家：依遺產數排序的國家清單＋搜尋框。
5. 類型：文化／自然／複合三欄切換；再可依登錄標準 i–x 篩選（附各標準的中文說明，下方提供）。
6. 年代：依登錄年（1978 起）分十年段。
7. 瀕危：danger=true 的清單。
8. 地圖：用 Leaflet（cdnjs 固定版本 1.9.4，OSM 圖磚）畫所有有 coord 的點，顏色依類型，點擊彈出卡片→單頁。
9. 搜尋：中英文名稱、國家即時篩選。
10. 單頁（#site/<id> 深連結，hashchange 支援）：主圖大圖＋其餘照片圖集（點開燈箱）；每張照片下方必須顯示「攝影：artist · 授權：license（連 license_url）· 來源：Wikimedia Commons（連 https://commons.wikimedia.org/wiki/File:<file>）」；標題中英文、國家（可點）、類型、登錄年／擴展年、登錄標準（徽章，hover 顯示說明）、瀕危狀態、跨國標記；intro（若無則顯示「介紹撰寫中」並顯示 en_desc 以小字＋註明「UNESCO 官方英文簡介（CC BY-SA 3.0 IGO）」）；highlights 條列；小地圖（Leaflet）；連結「UNESCO 官方頁」。上一處／下一處（同國家內）。
11. 無照片者顯示類型色的佔位圖並寫「照片待補」。
12. 頁尾：資料來源與授權說明（UNESCO 世界遺產名錄 CC BY-SA 3.0 IGO；照片來自 Wikimedia Commons，各依原授權；介紹文字由 AI 撰寫、經查核）；姊妹站連結：西洋藝術流派大全集 https://briantsaivc-web.github.io/art-history-atlas/、西洋雕刻演進大全集 …/sculpture-atlas/、希臘神話大全集 …/greek-myth-atlas/、聖經故事大全 …/bible-atlas/。
13. 手機寬度可用（16px 邊距、無水平捲動）；淺／深色主題切換照姊妹站。

## 登錄標準中文說明
i 人類創造天才的傑作；ii 在某時期或文化區內，對建築、技術、藝術、城鎮規劃或景觀設計的人類價值交流有重要影響；iii 為現存或已消逝的文化傳統或文明提供獨特或至少特殊的見證；iv 展現人類歷史重要階段的建築、建築群、技術組合或景觀的傑出範例；v 傳統人類聚落、土地或海洋利用的傑出範例，代表一種或多種文化與環境的互動；vi 與具普世意義的事件、活的傳統、思想、信仰或藝術文學作品有直接或實質關聯；vii 包含絕妙的自然現象或具罕見自然美與美學重要性的地區；viii 代表地球演化史主要階段的傑出例證；ix 代表陸地、淡水、海岸與海洋生態系統及動植物群落演化發展中重要且持續進行的生態與生物過程；x 包含生物多樣性就地保護最重要的自然棲地。

## 驗收（你可自驗）
- 用 python3 -m http.server 在 /home/claude/world-heritage-atlas 起服務，以 node + playwright（chromium 在 /opt/pw-browsers/chromium；/tmp/claude-0 已安裝 playwright）開首頁、#site/1、#site/2（zh 為 null 的例子）、各分頁，確認無 pageerror、資料載入成功、單頁顯示照片署名（若該處尚無照片則顯示佔位）。測完用獨立指令關掉伺服器（pkill 不要與其他指令同一行）。
- 回報：檔案大小、測試結果、未完成或待決事項。只寫 index.html（以及必要時的 data/meta.json 不要動）。不要 git commit。
