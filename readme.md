# UniversalScrapper

## 项目内容

通过抓取文件夹里的电影或电视剧并且与TMDB进行比对，实现匹配改名

## 针对的文件名范例

> Dogs.Without.Names.2015.HKG.BluRay.1080p.TrueHD.5.1.x265.10bit-CHD.mkv  
> Parents 1989 BluRay 1080p DTS-HD MA 2.0 x265.10bit-CHD

## 项目计划

- [x] 首先将文件名按空格和点进行分割处理
- [x] 首先对分割结果中的年份进行提取
- [x] 分割完成后利用TMDBapi进行逐个比对（从长到短）
- [ ] 首文件夹改名完成后进行子文件夹遍历检查（如果是TVs）
- [ ] 完毕后分类成功与失败（失败处理后续思考）