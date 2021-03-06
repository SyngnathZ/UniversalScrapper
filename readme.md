# UniversalScrapper

## 项目内容

通过抓取文件夹里的电影或电视剧并且与TMDB进行比对，实现匹配改名  
电影改名结果为"xxx (2021)的格式"  
电视剧改名结果为"xxx (2021)/Season xx的格式"

## 针对的文件名范例

> Dogs.Without.Names.2015.HKG.BluRay.1080p.TrueHD.5.1.x265.10bit-CHD.mkv  
> Parents 1989 BluRay 1080p DTS-HD MA 2.0 x265.10bit-CHD.mkv

## 支持的操作系统

> Windows  
> Linux（各种发行版）  
> Darwin (Mac OS)

## 使用方法

* 首先安装依赖 `pip install -r requirements.txt`
* 电影刮削使用方法：`python MoviesManager.py -p 待处理路径`
* 剧集刮削使用方法：`python TVsManager.py.py -p 待处理路径`

## 项目计划

- [x] 首先将文件名按空格和点进行分割处理
- [x] 首先对分割结果中的年份进行提取
- [x] 分割完成后利用TMDBapi进行逐个比对（从长到短）
- [x] 增加对多个影库结果刮削失败的移出操作
- [x] 增加对文件非法字符串的判断
- [x] 增加对TVs的支持
- [x] 首文件夹改名完成后进行子文件夹遍历检查（如果是TVs）
- [x] 完毕后分类成功与失败（失败处理后续思考）
- [x] 实现对剧集改名并且移动至（根目录/刮削完成/剧名 (20xx)/Season xx）
- [x] 实现对相同剧集的不同分辨率进行文件夹合并
- [x] 完全实现对文件夹内的nfo的利用

## 适配的特殊电影名

* Parents 1989 BluRay 1080p DTS-HD MA 2.0 x265.10bit-CHD.mkv——带空格的文件命名
* 1921.2021——即电影名是年份造成的bug
* Ten: The Sacrifice.2020.mkv——由于Windows下文件名非法字符造成的bug
* The.Wire.S02.2003.E10.BluRay.1080p.DTS.HDMA5.1.x265.10bit-CHD.mkv——剧集文件名内季信息单独分割出现