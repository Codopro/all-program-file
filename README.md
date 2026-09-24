# こどプロ 授業用配信ファイル

OneDrive で教室に公開している「こどプロ_授業用配信ファイル」の **バージョン管理用コピー**。
配信は引き続き OneDrive から行う。このリポジトリは変更履歴を残すためのもの。

- `CP_NN_program/` … NN月号（ベーシック／ベーシック2／ミドル／ミドル2／アドバンス）
- `ベーシック動画教材/` … ベーシックの授業動画（mp4 は Git LFS）
- `体験・スタートアップ/` … 体験会・SU 教材

OneDrive 上の zip（`CP_NN_program.zip` や SU 教材の zip）は **展開した状態** で保存している。
中身が同名フォルダ1段だけの zip はその1段をはがしている。

## 更新手順

1. OneDrive から最新版をダウンロードする（zip のままでよい）
2. education-school-analysis の同期スクリプトに通す

   ```
   PYTHONIOENCODING=utf-8 python internal/claude/scripts/sync_cp_program_git.py --src <ダウンロードしたzip> --commit --push
   ```
