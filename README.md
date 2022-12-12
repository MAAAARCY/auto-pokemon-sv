# auto-pokemon-sv
スイッチのBluetooth疑似コントローラプロジェクトの   
https://github.com/mart1nro/joycontrol   
と、それを拡張した   
https://github.com/Almtr/joycontrol-pluginloader   
を派生させ、ポケモンSVに対応させたプロジェクトです。

現在は卵を集める作業と孵化する作業で分離されていますが、将来的に卵収集→孵化厳選に遷移できるようにする予定です。

## 使い方
### HatchEggs.py
#### 概要
5分間孵化作業を行うプログラムです。5分にした理由は、孵化に必要な歩数が多いポケモンで５個孵化するのに必要な時間が4分半だったからです。

1. 手持ちの先頭に孵化要員（特性ほのおのからだ等）を置いて卵を5個持つ
2. ライド状態を解除して以下のコマンドを実行(XX:XX:XX:XX:XX:XXはSwitchのMACアドレス)
```shell
cd ~/AutoPokemonSV/
sudo joycontrol-pluginloader -r XX:XX:XX:XX:XX:XX hatch-eggs/HatchEggs.py
```
### GenerateEggs.py
#### 概要
ピクニックを開始し、スーパーピーナッツバターサンドを制作してバスケットに入れられた卵を30分間回収し続けるプログラムです。

1. メニューのカーソルをバックに合わせ、以下の写真の位置でレポート
2. メニューをとじて以下のコマンドを実行
```shell
cd ~/AutoPokemonSV/
sudo joycontrol-pluginloader -r XX:XX:XX:XX:XX:XX generate-eggs/GenerateEggs.py
```
