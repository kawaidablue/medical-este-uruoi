# メディカルエステうるおい — デザイン仕様（Figma / コーディング引き継ぎ）

最終的なソースは本パッケージ（HTML/CSS/build.py/img）です。Figmaで再構成・実装する際の基準値をまとめます。

## 1. ページ一覧
| ファイル | 内容 | 実サイト元 |
|---|---|---|
| index.html | トップ | クライアント提供HTML（base64画像埋め込み・自己完結） |
| treatment-shimi.html | シミ・肝斑（メソアクティス） | /spot/ |
| treatment-nikibi.html | ニキビ（水素水ピーリング） | /acne/ |
| treatment-shiwa.html | しわ・たるみ（スマスアップNEO） | /wrinkle/ |
| treatment-hari.html | ハリ・ツヤ（エンビロン） | /glowing/ |
| price.html | 料金表 | 各ページ実価格を集約 |
| voice.html | お客様の声 | /voice/（取得不安定・2件のみ反映） |
| cosmetics.html | 化粧品 | /cosme/（実商品・価格反映、verilab.jp/shop連携） |

※ index.html はクライアントHTML。treatment-*/price/voice/cosmetics は build.py が style.css を inline 展開して生成。

## 2. カラートークン
| 役割 | 変数 | HEX |
|---|---|---|
| ページ背景 | cream | #F6F1E6 |
| セクション地色（ivory） | beige | #EFE7D6 |
| 濃い帯（greige） | beige-dk | #E7DCC6 |
| セージ地（CTA背景等） | green-bg | #E7EBDD |
| 白 | white | #FFFFFF |
| 見出し文字 | ink | #3A332A |
| 小見出し | ink-2 | #4A4236 |
| 本文 | ink-soft | #6B5F4B |
| アクセント（セージ） | green | #8C9A6B |
| 濃セージ（主役ボタン/価格/筆記体） | green-dk | #6E7C4E |
| 補助文字 | taupe | #8C7E63 |
| ロゴ文字 | teal | #48B399 |
| ロゴアイコン | blue | #028DC6 |
| 罫線 | line | #E0D8C6 |
| 薄罫線 | line-soft | #EAE3D3 |
| LINE（ブランド色） | — | #06C755 |

影: shadow `0 24px 60px -28px rgba(74,66,52,.40)` ／ shadow-sm `0 14px 34px -22px rgba(74,66,52,.34)`

## 3. フォント（Google Fonts）
| 役割 | フォント |
|---|---|
| 英字の装飾・透かし見出し | Cormorant Garamond |
| 和文見出し | Shippori Mincho |
| 本文・サンセリフ | Zen Kaku Gothic New |
| 筆記体ラベル（Reservation等） | Parisienne |

- 数字・価格・電話番号は Zen Kaku Gothic New ではなく **Cormorant Garamond（軽め・控えめサイズ）** を使用。
- 施術名ラベル（英字）は **サンセリフ大文字＋字間広め（緑）** で統一。

## 4. 主要コンポーネント
- **ヘッダー**: 透過クリーム＋blur、左=ロゴ、右=円形ハンバーガー（丸＋3本線＋MENU）。
- **ハンバーガーメニュー（全画面オーバーレイ）**: 左=ロゴ＋コンセプト＋電話/受付/住所＋SNS（デスクトップはボタニカルの枝）、右=和文＋英字サブラベルのリスト。開く=ボタン、閉じる=右上×。項目はスタッガーでフェードイン。z-index はヘッダーより前面。
- **ページヒーロー（サブ共通）**: 写真＋薄クリームのベール＋筆記体EN＋和文h1＋リード（パンくず無し）。
- **セクション見出し**: 背景に大きな英字透かし（Cormorant, bronze .15）＋筆記体（Parisienne）＋和文タイトル（Shippori Mincho）。
- **施術ページ構成**: ヒーロー →（お悩みチェック）→ 〜とは → 種類/topics → 施術について（施術内容＋熱効果/電気刺激＋縦STEP流れ＋動画＋症例＋注意を集約）→ 声 → 料金 → FAQ → 関連 → 予約。
- **背景**: 全セクション cream に統一（色の交互なし）。区切りは見出し・余白・白カードで表現。
- **料金表**: ジャンプ目次＋カテゴリ別（写真サムネ＋見出し）＋初回限定の強調バー＋税抜/税込併記のテーブル（ストライプ）。
- **製品カード**: 写真＋タグ＋名称＋価格（大きめ）、ホバーで浮く＋画像ズーム。
- **予約セクション（全ページ共通）**: セージ→クリームのグラデ、白カードを左右2分割（左=電話／右=WEB予約[緑塗り]＋LINE[白地＋緑枠＋吹き出し]＋SNS）。
- **フッター**: 4カラム（ブランド/Menu/About/Link）＋コピーライト。全ページ共通。

## 5. レスポンシブ
- 主要グリッドは 760〜920px 付近で 1〜2カラムへ。メニューはモバイルで縦積み＋下部に連絡先。

## 6. 公開前に要対応（素材・情報待ち）
- [ ] ヒーロー画像の **Adobe Stock 透かし** → ライセンス版へ差し替え（index.html の hero base64／サブの img/hero.jpg）
- [ ] 仮写真（商品・施術・症例・スタッフ・店内）→ 実写真へ
- [ ] お知らせ（News）の仮の日付・項目 → 実内容へ
- [ ] `href="#"` のリンク（WEB予約／LINE／SNS／お知らせ一覧）→ 実URL
- [ ] LINEボタン → 公式ボタン画像に差し替え可（現状は白地＋緑枠の代替）
- [ ] お客様の声 → 実データを追加（現状2件）
- [ ] 文言・価格・医療表現は最終的にクライアント確認

## 7. ビルド方法
```
cd uruoi
python3 build.py   # style.css を読み込み、treatment-*/price/voice/cosmetics を生成
```
index.html は build 対象外（クライアントHTMLをそのまま採用）。
