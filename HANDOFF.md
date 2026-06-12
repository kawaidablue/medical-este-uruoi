# 引き継ぎ書 — メディカルエステ うるおい サイト制作

最終更新: 2026-06-09（施術3ページ実装後） / このファイルと `uruoi/` フォルダ一式を次のチャットにアップロードすれば続きから作業できます。

---

## 0. 次のチャットで最初にやること
1. `uruoi/` フォルダ（`build.py` / `style.css` / `img/` / 各 .html）をアップロードする。
2. 作業ディレクトリを作って中身を展開し、`python3 build.py` が通ることを確認する。
   - 出力先は `OUT = /mnt/user-data/outputs/uruoi`（build.py 冒頭で定義）。
3. 主対象は **`treatment-shimi.html`（雛形・完成度高）**。これをテンプレートに他ページを仕上げる。

> 注意: `/home/claude` はセッションごとにリセットされる。だから build.py / img は必ず再アップロードが必要。

---

## 1. プロジェクト概要
- クライアント: メディカルエステうるおい（medical-este-uruoi.com）
- 目的: 既存サイトのリニューアル。**トップページ（クライアント提供の完成HTML）に下層ページを合わせ込む**。
- 下層ページ: 施術ページ（シミ・肝斑＝完成度高、ニキビ/しわたるみ/ハリツヤ＝枠のみ）、お客様の声、料金表、化粧品。

### 参照素材（過去にアップ済み・必要なら再依頼）
- `top-7.png` / `top-9.png` … トップページのスクショ（デザイン基準）
- トップの**完成HTMLコード**（自己完結・CSS内蔵）をユーザーがチャットに貼付済み = サイトの最終デザイン基準
- `シミ_断面図.jpg` … 「シミのしくみ」断面図（→ `img/skin_diagram.jpg` に取込済み）
- `シミ_下の段の絵.jpg` … 種類別の顔イラスト集（→ 切り出して `img/ty_solar/freckle/melasma.jpg` に取込済み）

---

## 2. ビルドシステム
- `build.py` … 全ページを生成する Python スクリプト。`python3 build.py` で `OUT` に全 .html + style.css を出力。
- `style.css` … 下層ページ共通スタイル（build.py がコピーする運用。編集は build.py 横の style.css を直接編集 → `cp style.css {OUT}/style.css`）。
- `img/` … 画像。build.py が起動時に `img/*.jpg|png` を全部 base64 で `IMGDATA` に読み込み、`photo(key)` でローカル埋め込み（外部依存なし）。**キー = ファイル名（拡張子なし）**。

### 主要関数（build.py 内）
- `photo(key, w=900)` → `<img class="ph" src="data:...">`（base64埋め込み）
- `mfill(theme, vw, vh, motif, imgkey, w)` → media枠（写真＋フォールバックSVG）
- `khead(jp, en)` → **大きい中央ウォーターマーク見出し**（英字大＋Parisienne筆記体＋和文）= トップの `.shead` 様式
- `khead2(jp, en)` → **小さい左寄せ補足見出し**（Parisienne＋和文＋右へ伸びる罫線）
- `hero_full(meta, th)` → 全面背景写真ヒーロー（タイトルのみ・案B採用）
- `treatment_page(meta)` → 施術ページ雛形（下記セクション順）
- `page(title, body)` → header + body + RESERVE + FOOTER でラップ
- `index_page()` → 旧・自前トップ（緑基調・**古い/破棄推奨**。実トップはユーザー提供HTMLを使う）

---

## 3. デザインシステム（★トップに合わせて確定）
`style.css :root` の値（CSS変数名は旧来のままだが、値をトップのトークンに差し替え済み）:

| 変数 | 値 | 用途 |
|---|---|---|
| --cream | #F6F1E6 | ページ背景 |
| --beige | #EFE7D6 | セクション地（ivory） |
| --beige-dk | #E7DCC6 | 帯（greige） |
| --green-bg | #E7EBDD | セージ系セクション |
| --ink | #3A332A | 主見出し（brown） |
| --ink-2 | #4A4236 | 小見出し |
| --ink-soft | #6B5F4B | 本文 |
| --green | #8C9A6B | セージ・アクセント（bronze） |
| --green-dk | #6E7C4E | 濃セージ（bronze-deep） |
| --taupe | #8C7E63 | 補助テキスト |
| --teal #48B399 / --blue #028DC6 | ロゴ色 |

**フォント**（Google Fonts / build.py の FONTS でロード）:
- 英字装飾: Cormorant Garamond（`--serif-en`）
- 和文見出し: Shippori Mincho（`--serif-jp`）
- 和文本文・UI: **Zen Kaku Gothic New**（`--body-jp` / `--sans-jp`）
- 緑の筆記体（見出しの英字スクリプト等）: **Parisienne**（`--script`）

**ボタン**: `.btn-solid`=白地＋茶文字＋#C3B79C罫線＋影（角丸8px）／`.btn-line`=茶罫線／`.btn-green`=緑アウトライン。
**ヘッダー**: 固定・半透明＋blur、ロゴ左＋ハンバーガー（MENUラベルはCormorant）。
**フッター**: アイボリー4カラム、見出しは大文字レタースペース、コピーライトはCormorant。

---

## 4. シミ・肝斑ページ（treatment-shimi.html）構成 ★確定
（`treatment_page(meta)` が meta に応じて下記を生成）

1. **ヒーロー** `hero_full` … 全面写真＋白タイトルのみ（案B）。リード文・料金表示は無し。
2. **メソアクティス紹介** … 中央 khead（Mesoactis）＋本文3段＋提携クリニックリンク。
3. **シミとは** … 中央 khead（About）＋本文＋**実物断面図**（`img/skin_diagram.jpg`／`.skin-fig` 全幅カード）。
4. **シミの種類** … 中央 khead（Type）＋3行（日光黒子/雀卵斑/肝斑）。各行に**切出しイラスト**（`ty_solar/ty_freckle/ty_melasma`、`.type-photo` 丸角・トーン無し）。
5. **シミ・肝斑の施術** … 中央 khead（Treatment）＋写真split＋メソアクティス説明。
6. **施術の解説動画** … 中央 khead（Movie）＋動画枠2つ（`.videos`／再生ボタン付プレースホルダ＝実YouTube埋込に差替）。
7. **施術の流れ** … 中央 khead（Step）＋縦タイムライン（`.flow-tl`、番号はイタリック無し）。
8. **施術の症例写真** … **小見出し khead2（Case）**＋点線枠プレースホルダ「只今準備中です。」
9. **ご注意ください** … **小見出し khead2（Notice）**＋白カード2カラム（左:副作用・リスク／右:禁忌事項）。※旧「副作用・リスク」「禁忌事項」を統合。
10. **施術のお客様の声** … `.section green`＋ボタン「さらにお客様のお声を見る」→ voice.html
11. **施術の料金** … 中央 khead（Price）＋初回限定強調ボックス＋通常メニュー表。
12. **施術のよくある質問** … 中央 khead（Question）＋Q&Aカード（円形Q番号・イタリック無し）。
13. **ほかのお悩み・施術** … 中央 khead（Menu）＋関連カード3枚（ニキビ/しわたるみ/ハリツヤへリンク）。
14. **RESERVATION**（予約・電話）＋ **Footer**（page() が付与）。

### meta のキー（shimi 参照）
`title, crumb, theme, motif, hero_img, img1_key, h1, lead(未使用), intro_price(未使用),
method_label, method_en, intro_paras[], clinic_link(text,url), whatis(title,text),
types[(name,desc,pattern)], treatment(label,desc), videos[title...],
flow[(step,desc)], cases(str), risks(str), contra[str...], voice_more(bool),
pricing{first{name,was,now,tax}, menu[(name,price,tax)]}, faq[(q,a)...], related[(en,jp,href,theme,motif,imgkey)]`

---

## 5. 確定したデザイン決定（経緯）
- ヒーロー: 案2＝**全面写真＋白タイトルのみ**を採用（案A:クリーム地＋右写真は不採用）。
- 見出しに**強弱**: 主要=大きい中央ウォーターマーク、補足(症例/注意)=小さい左寄せ。連続セクションの単調さ対策。
- 「副作用・リスク」＋「禁忌事項」=**1セクション2カラムに統合**。
- 数字（流れ01〜/QのQ1〜）は**イタリックをやめ**まっすぐな字形。
- 小さい緑の筆記体ラベルは **Parisienne**。
- 「シミとは」図=**実物断面図**に差替。「シミの種類」=**実物イラストを切出し**て使用（トーン無し）。
- サブページ全体を**トップのトークン**（配色・フォント・見出し・ボタン・フッター）に合わせ込み済み。

---

## 6. img/ アセット（主なもの）
- 共通: logo.png, hero.jpg, texture.jpg, serum.jpg, cleanse.jpg, cream.jpg, smear.jpg
- シミ用: skin_diagram.jpg（断面図）, ty_solar.jpg/ty_freckle.jpg/ty_melasma.jpg（種類イラスト）
- 旧トップ(index.html)用: home_*.jpg, te_*.jpg（※index.htmlは破棄予定なら不要）
> 多くは無料素材のプレースホルダ。実写真・実症例に差替前提。

---

## 7. 残作業（PENDING）
1. **残り3ページ仕上げ … ✅ 完了（2026-06-09）**: treatment-nikibi / treatment-shiwa / treatment-hari を、シミと同じ構成（イントロ/とは/種類/施術/動画/流れ/症例/注意/声/料金/FAQ/関連）でフル実装済み。
   - 各ページの meta（build.py 内 `nikibi` / `shiwa` / `hari`）に全キーを投入。テキストはダミーの仮原稿 → **クライアント確認・差替前提**。
   - 料金は price.html と整合させた仮値。実価格はクライアント確認のこと。
   - **build.py を汎用化済み**: ①「〜とは」図版は `whatis_img` キーがある時だけ表示（shimi のみ skin_diagram、他3ページは図版なし＝テキストのみ）。②「種類」は `ty_<pattern>` 画像が無ければテキストのみ行（`.type-row.text-only`、左に緑のアクセント罫線）。③施術見出しは `treatment_title`、eyebrow は `method_en` で可変。
   - 残素材: nikibi/shiwa/hari 用の「〜とは」図版・種類イラスト・実症例・実写真。クライアント提供が望ましい。
2. **トップの扱い … 確定（2026-06-09）**: クライアント提供の本物トップHTMLを `index.html` として採用。build.py はトップを生成しない（home_page()/index_page() の書き出しを停止、関数はテンプレ参照用に温存）。
   - 巨大 base64 だった3点のみローカル参照化: ロゴ=`img/logo.png`、ヒーロー=`img/te_hero.jpg`、院長=`img/te_doctor.jpg`（実写真が来たらこの3ファイルを差替）。
   - お悩みカード/Pick up/コンセプト/施術内容の写真は**元コードどおり unsplash 外部URL参照**（実ブラウザで表示。オフラインでは空白）。必要ならローカル埋め込みに変更可。
   - リンク接続済み: メニュー4カード・施術内容「詳しく見る」・フッターMenu → 各 treatment-*.html、料金表 → price.html、症例 → voice.html。ハンバーガーメニューにも下層リンク追加。
   - **index.html は自己完結化（2026-06-10）**: ロゴ・ヒーローは base64 で本文に埋め込み済み（単体・プレビューでも表示可、相対 `img/` 不要）。約147KB。
   - お悩みカード/Pick up/コンセプト/施術内容の写真のみ unsplash 外部URL参照のまま（オンライン表示）。ヒーローは Adobe Stock 透かしありのため公開前に差替。
   - ごあいさつ欄は写真なしレイアウトに変更・代表 豊田崇大の文言に差替済み。
   - **実ロゴ・実ヒーロー反映済み（2026-06-10）**: `img/logo.png`（透過200×50）、`img/hero.jpg`（1440×900 フル構図）。ヒーローは右62%切り出しをやめ、フル幅1枚絵＋左にテキスト重ねの構成に変更（top-9.png 一致）。
   - ⚠️ ヒーロー画像に Adobe Stock の透かしあり。公開前にライセンス版へ `img/hero.jpg` を差替。院長写真は未提供のため `img/te_doctor.jpg`（仮）のまま。

3. voice / price / cosmetics ページ … 旧形式が残っている可能性。新トークンで再整備。
4. 動画枠 → 実YouTube埋込、症例「準備中」→ 実症例、各写真 → 実写真へ差替。
5. 各ページの料金・症例・原稿はすべて**仮**。本番前にクライアント監修（特に医療・効果に関わる表現、禁忌・副作用の記載）を受けること。

---

## 8. 技術メモ / 注意
- ネットワーク制限あり（外部画像URLは取得不可。画像はローカル base64 埋込が確実）。Unsplash等のCDNは不可。
- Google Fonts はランタイムロード。**スクリーンショット環境ではフォントが代替表示**になる（ブラウザでは正しく出る）。
- Playwright フルページ撮影で `loading="lazy"` 画像が出ないことがある（実表示は問題なし）。確認時はスクロールしてから撮る。
- 2倍解像度のフル撮影は Chromium の最大画像高さ(~16384px)を超えると下部が白くなる。dsf=1 か分割で撮る。
- `.reveal` は IntersectionObserver制御。撮影時は `document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))` で強制表示。

---

## 9. ビルド/確認コマンド
```bash
cd <uruoiを展開したディレクトリ>
python3 build.py            # → /mnt/user-data/outputs/uruoi に出力
cp style.css /mnt/user-data/outputs/uruoi/style.css   # style.css を編集した場合
```
