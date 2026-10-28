# 世界遺產介紹撰寫指令（給子代理）
輸入：指定的 /home/claude/world-heritage-atlas/work/intro/batch_NN.json（每處：id、en 英文名、zh 中文名（可能 null）、countries、cat、criteria、year、ext、danger、en_desc＝UNESCO 官方英文簡介）。

每處產出：
- zh：若輸入 zh 為 null，給台灣慣用的繁體中文正式名稱（依官方英文名忠實翻譯；台灣常見譯名優先）；輸入已有 zh 則原樣回傳，除非明顯是簡體或錯字（才修正並在 zh_note 說明）。
- intro：300–450 字繁體中文，一般文體（不刻意簡化、不浮誇、不用驚嘆號）。內容依序：它是什麼、在哪裡；為何具普世價值（對應其登錄標準）；歷史或自然形成脈絡；現況（若 danger=true，說明列入瀕危的原因，只寫有把握的）。
- highlights：3–5 條，每條 12–30 字，參觀或認識時最值得注意的重點。
- 事實紀律：只寫 en_desc 中有的、或你非常有把握的常識事實。不要編造數字（面積、年代、高度、人數），沒把握就不寫數字。不要寫門票、交通、開放時間。台灣讀者用語（例如「公尺」「公里」）。

輸出：/home/claude/world-heritage-atlas/work/intro/out_NN.json，陣列 [{"id","zh","zh_note":null|"...","intro","highlights":[...]}]，與輸入同序同筆數。
驗收（你可自驗）：python 讀回確認筆數、id 一致、intro 長度 250–500 字、highlights 3–5 條、全為繁體（用 opencc 's2t'（字元級，不要用 s2twp 詞彙轉換）檢查：若轉換後有差異代表混入簡體字，只修正那些字；台灣用語如「登錄」「保存」「分布」維持原樣）。
回報：完成筆數、補了幾個中文名、3 處最沒把握的事實（id＋內容）。只寫該輸出檔。

暫存檔一律放在你專屬的資料夾 /tmp/claude-0/intro_NN/（NN 為批次號），不要使用或覆寫其他資料夾的檔案。
