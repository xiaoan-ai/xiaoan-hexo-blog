---
title: AndroidApp加固与脱壳
date: 2023-04-09T12:00:00+08:00
categories:
  - 移动安全
tags:
  - Android
  - 加固
  - 脱壳
---

# 0x01 APP加固
## 01.为什么要加固
APP加固是对APP代码逻辑的一种保护。原理是将应用文件进行某种形式的转换，包括不限于隐藏，混淆，加密等操作，进一步保护软件的利益不受损坏。总结主要有以下三方面预期效果：

**1.防篡改：**通过完整性保护和签名校验保护，能有效避免应用被二次打包，杜绝盗版应用的产生；**2.防逆向：**通过对代码进行隐藏以及加密处理，使攻击者无法对二进制代码进行反编译，获得源代码或代码运行逻辑；**3.防调试：**通过反调试技术，使攻击者无法调试原生代码或Java代码，阻止攻击者获取代码里的敏感数据。

## 02.APP加固技术发展历程
![图片.png](https://cdn.nlark.com/yuque/0/2023/png/29674331/1681027325669-b2bec0ae-f72d-4bf3-96d3-bc1615b49d5b.png#averageHue=%23ccdbe9&clientId=u730e4549-c8cd-4&from=paste&height=278&id=u814e2aaf&name=%E5%9B%BE%E7%89%87.png&originHeight=417&originWidth=1046&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=444276&status=done&style=none&taskId=ub875750f-f0dd-4bb4-8d29-85b8e69cfa4&title=&width=697.3333333333334)

### 1.动态加载
Android动态加载加固技术用于保护App应用的逻辑不被逆向与分析，最早普遍在恶意软件中使用，它主要基于Java虚拟机提供的动态加载技术。由于动态加载技术主要依赖于java的动态加载机制，所以要求关键逻辑部分必须进行解压，并且释放到文件系统。这种动态加载技术不足之处在于：1.这一解压释放机制就给攻击者留下直接获取对应文件的机会；2.可以通过hook虚拟机关键函数，进行dump出原始的dex文件数据。

### 2.不落地加载
Android不落地加载技术，它是在动态加载技术的基础进行改进。它通过借鉴第一代加固的动态加载技术中，关键逻辑部分必须释放到文件系统的缺陷，它主要新增文件级别的加解密。

文件级别的加解密技术主要有两种实现方案：1.通过拦截系统的IO相关函数，在这些系统的函数中进行透明加解密。2.直接调用虚拟机提供的函数，进行不落地的加载。这种文件级别的加解密不足之处在于：1.由于在App启动时需处理大量加解密操作，它会造成App启动卡顿假死或黑屏现象，用户体验感较差；2.由于它的内存是连续的，通过hook关键函数就可以获取到连续完整的dex数据。

### 3.指令抽取
android的指令抽取，主要在于函数基本的抽取保护。通过使用android虚拟机自带的解释器进行执行代码。将原始App中dex文件的函数内容进行清除，并将单独移动到一个加密文件中，在App运行的时候，再将函数内容重新恢复到对应的函数体。

这一指令抽取技术的不足之处在于：1.使用大量的虚拟机内部结构，会出现兼容性问题；2.使用android虚拟机进行函数内容的执行，无法对抗自定义虚拟机；3.它跟虚拟机的JIT优化出现冲突，达不到最佳的性能表现。

### 4.指令转换/VMP
它主要通过实现自定义Android虚拟机的解释器，由于自定义解释器无法对Android系统内的其他函数进行直接调用，所有必须使用java的jni接口进行调用。

这种实现技术主要有两种实现：1.dex文件内的函数被标记为native，内容被抽离并转换为一个符合jni要求的动态库。2.dex文件内的函数被标记为native，内容被抽离并转换为自定义的指令格式。并通过实现自定义接收器，进行执行代码。它主要通过虚拟机提供的jni接口和虚拟机进行交互。这一指令转换技术实现方案不足之处在于：在攻击者面前，攻击者可以直接将这个加固技术方案当做黑盒，通过实现自定义的jni接口对象进行内部调试分析，从而得到完整的原始dex文件。

### 5.虚拟机源码保护
通过利用虚拟机技术保护App中的所有代码，包括java、Kotlin、C/C++等多种代码，虚拟机技术主要是通过把核心代码编译成中间的二进制文件，随后生成独特的虚拟机源码，保护执行环境和只有在该环境下才能执行的运行程序。通过基于llvm工具链实现ELF文件的vmp保护。通过虚拟机保护技术，让ELF文件拥有独特的可变指令集，大大提高了指令跟踪，逆向分析的强度和难度。

## 03.常规加固方式以及常见加固特征辨别
### 1.DEX安全加固
VMP虚拟机保护

java2C保护

DEX函数抽取加密

### 2.so库加固
so代码高级加密

so函数动态加密

防hook攻击

防脱壳

### 3.资源文件加固
assets资源文件加密

H5文件加密

XML配置文件保护

### 4.防调试加固
防动态调试

防内存DUMP

防动态注入

### 5.数据保护加固
防日志泄露

防截屏保护

数据文件加密

加密算法保护

### 6.常见加固特征收集

```
娜迦： libchaosvmp.so, libddog.so，libfdog.so
爱加密：libexec.so,libexecmain.so，ijiami.dat
梆梆： libsecexe.so,libsecmain.so , libDexHelper.so
360：libprotectClass.so,libjiagu.so， libjiagu_art.so，libjiagu_x86.so
通付盾：libegis.so，libNSaferOnly.so
网秦：libnqshield.so
百度：libbaiduprotect.so
腾讯：libshellx-2.10.6.0.so，libBugly.so，libtup.so, libexec.so，libshell.so
阿里聚安全：aliprotect.dat，libsgmain.so，libsgsecuritybody.so
腾讯御安全：libtosprotection.armeabi.so，libtosprotection.armeabi-v7a.so，libtosprotection.x86.so
网易易盾：libnesec.so
APKProtect:libAPKProtect.so
几维安全：libkwscmm.so, libkwscr.so, libkwslinker.so

```

## 03.app加壳原理解析
上面提到的加固方式每一个都有可讨论的点，这里我们就其中比较重要的加壳这一加固方式进行探讨。

### 1.原理图
![图片.png](https://cdn.nlark.com/yuque/0/2023/png/29674331/1681027351192-46d18b42-9fc8-4776-a40f-4fbab61739be.png#averageHue=%23fbfbfb&clientId=u730e4549-c8cd-4&from=paste&height=250&id=u8f1ef298&name=%E5%9B%BE%E7%89%87.png&originHeight=375&originWidth=953&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=44922&status=done&style=none&taskId=uead84d7e-2392-4c10-97ab-213beaff073&title=&width=635.3333333333334)

如图知道，我们在加固的过程中需要三个对象：

```
1、需要加密的Apk(源Apk)
2、壳程序Apk(负责解密Apk还原并执行)
3、加密工具(将源Apk进行加密和壳Dex合并成新的Dex)

```

主要步骤为：

```
1. 拿到需要加密的Apk和自己的壳程序Apk
2. 用加密算法对源Apk进行加密
3. 将壳Apk进行合并得到新的Dex文件
4. 最后替换壳程序中的dex文件即可得到新的App

```

这个新的Apk叫作脱壳程序Apk,他的主要工作是：负责解密源Apk.然后加载Apk,让其正常运行起来。

### 2.DEX文件
这其中很重要的一步就是如何加密合并得到新的DEX文件，因此简单介绍一下Dex文件的格式。

![图片.png](https://cdn.nlark.com/yuque/0/2023/png/29674331/1681027358615-2d37229f-7e25-4e7f-b85b-753736090f67.png#averageHue=%23f3f1f0&clientId=u730e4549-c8cd-4&from=paste&height=575&id=u6c5d719a&name=%E5%9B%BE%E7%89%87.png&originHeight=863&originWidth=1406&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=462231&status=done&style=none&taskId=u6785ea23-f6ff-42be-9e69-ca34770e543&title=&width=937.3333333333334)

关注上面红色标记的三个部分：因为我们需要将一个文件(加密之后的源Apk)写入到Dex中，那么我们只需要修改：

文件校验码(checksum)：因为他是检查文件是否有错误。

signature：也是唯一识别文件的算法。

dex文件的大小：file_size

```
1) checksum
文件校验码 ，使用alder32 算法校验文件除去 maigc ，checksum 外余下的所有文件区域 ，用于检查文件错误

2) signature
使用 SHA-1 算法 hash 除去 magic ,checksum 和 signature 外余下的所有文件区域 ，用于唯一识别本文件

3) file_size
Dex文件的大小

```

**注意：因为我们在脱壳的时候，需要知道Apk的大小，才能正确的得到Apk。所以需要将这个值放到文件的末尾。**

总结一下我们需要做：修改Dex的三个文件头，将源Apk的大小追加到壳dex的末尾。

我们修改之后得到新的Dex文件样式如下：

![图片.png](https://cdn.nlark.com/yuque/0/2023/png/29674331/1681027366018-ce1a6892-d4d1-47b0-8abd-0f62355f458f.png#averageHue=%23fef0ef&clientId=u730e4549-c8cd-4&from=paste&height=254&id=ue7ca8bda&name=%E5%9B%BE%E7%89%87.png&originHeight=381&originWidth=636&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=39779&status=done&style=none&taskId=ue75da1a2-7402-47ad-94b9-c489ab3d575&title=&width=424)

### 3.加壳/加密程序
涉及到的核心代码：

```
package com.example.reforceapk;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.zip.Adler32;

public class mymain {
 /**
 * @param args
 */
 public static void main(String[] args) {
 // TODO Auto-generated method stub
 try {
 File payloadSrcFile = new File("force/ForceApkObj.apk"); //需要加壳的程序
 System.out.println("apk size:"+payloadSrcFile.length());
 File unShellDexFile = new File("force/ForceApkObj.dex"); //解客dex
 byte[] payloadArray = encrpt(readFileBytes(payloadSrcFile));//以二进制形式读出apk，并进行加密处理//对源Apk进行加密操作
 byte[] unShellDexArray = readFileBytes(unShellDexFile);//以二进制形式读出dex
 int payloadLen = payloadArray.length;
 int unShellDexLen = unShellDexArray.length;
 int totalLen = payloadLen + unShellDexLen +4;//多出4字节是存放长度的。
 byte[] newdex = new byte[totalLen]; // 申请了新的长度
 //添加解壳代码
 System.arraycopy(unShellDexArray, 0, newdex, 0, unShellDexLen);//先拷贝dex内容
 //添加加密后的解壳数据
 System.arraycopy(payloadArray, 0, newdex, unShellDexLen, payloadLen);//再在dex内容后面拷贝apk的内容
 //添加解壳数据长度
 System.arraycopy(intToByte(payloadLen), 0, newdex, totalLen-4, 4);//最后4为长度
 //修改DEX file size文件头
 fixFileSizeHeader(newdex);
 //修改DEX SHA1 文件头
 fixSHA1Header(newdex);
 //修改DEX CheckSum文件头
 fixCheckSumHeader(newdex);

 String str = "force/classes.dex";
 File file = new File(str);
 if (!file.exists()) {
 file.createNewFile();
 }
 
 FileOutputStream localFileOutputStream = new FileOutputStream(str);
 localFileOutputStream.write(newdex);
 localFileOutputStream.flush();
 localFileOutputStream.close();

 } catch (Exception e) {
 e.printStackTrace();
 }
 }
 
 //直接返回数据，读者可以添加自己加密方法
 private static byte[] encrpt(byte[] srcdata){
 for(int i = 0;i= 0; i--) {
 b[i] = (byte) (number % 256);
 number >>= 8;
 }
 return b;
 }

 /**
 * 修改dex头 sha1值
 * @param dexBytes
 * @throws NoSuchAlgorithmException
 */
 private static void fixSHA1Header(byte[] dexBytes)
 throws NoSuchAlgorithmException {
 MessageDigest md = MessageDigest.getInstance("SHA-1");
 md.update(dexBytes, 32, dexBytes.length - 32);//从32为到结束计算sha--1
 byte[] newdt = md.digest();
 System.arraycopy(newdt, 0, dexBytes, 12, 20);//修改sha-1值（12-31）
 //输出sha-1值，可有可无
 String hexstr = "";
 for (int i = 0; i mAllApplications = (ArrayList) RefInvoke
 .getFieldOjbect("android.app.ActivityThread",
 currentActivityThread, "mAllApplications");
 mAllApplications.remove(oldApplication);//删除oldApplication
 
 ApplicationInfo appinfo_In_LoadedApk = (ApplicationInfo) RefInvoke
 .getFieldOjbect("android.app.LoadedApk", loadedApkInfo,
 "mApplicationInfo");
 ApplicationInfo appinfo_In_AppBindData = (ApplicationInfo) RefInvoke
 .getFieldOjbect("android.app.ActivityThread$AppBindData",
 mBoundApplication, "appInfo");
 appinfo_In_LoadedApk.className = appClassName;
 appinfo_In_AppBindData.className = appClassName;
 Application app = (Application) RefInvoke.invokeMethod(
 "android.app.LoadedApk", "makeApplication", loadedApkInfo,
 new Class[] { boolean.class, Instrumentation.class },
 new Object[] { false, null });//执行 makeApplication（false,null）
 RefInvoke.setFieldOjbect("android.app.ActivityThread",
 "mInitialApplication", currentActivityThread, app);

 ArrayMap mProviderMap = (ArrayMap) RefInvoke.getFieldOjbect(
 "android.app.ActivityThread", currentActivityThread,
 "mProviderMap");
 Iterator it = mProviderMap.values().iterator();
 while (it.hasNext()) {
 Object providerClientRecord = it.next();
 Object localProvider = RefInvoke.getFieldOjbect(
 "android.app.ActivityThread$ProviderClientRecord",
 providerClientRecord, "mLocalProvider");
 RefInvoke.setFieldOjbect("android.content.ContentProvider",
 "mContext", localProvider, app);
 }
 
 Log.i("demo", "app:"+app);
 
 app.onCreate();
 }
 }

 /**
 * 释放被加壳的apk文件，so文件
 * @param data
 * @throws IOException
 */
 private void splitPayLoadFromDex(byte[] apkdata) throws IOException {
 int ablen = apkdata.length;
 //取被加壳apk的长度 这里的长度取值，对应加壳时长度的赋值都可以做些简化
 byte[] dexlen = new byte[4];
 System.arraycopy(apkdata, ablen - 4, dexlen, 0, 4);
 ByteArrayInputStream bais = new ByteArrayInputStream(dexlen);
 DataInputStream in = new DataInputStream(bais);
 int readInt = in.readInt();
 System.out.println(Integer.toHexString(readInt));
 byte[] newdex = new byte[readInt];
 //把被加壳apk内容拷贝到newdex中
 System.arraycopy(apkdata, ablen - 4 - readInt, newdex, 0, readInt);
 //这里应该加上对于apk的解密操作，若加壳是加密处理的话
 //?
 
 //对源程序Apk进行解密
 newdex = decrypt(newdex);
 
 //写入apk文件 
 File file = new File(apkFileName);
 try {
 FileOutputStream localFileOutputStream = new FileOutputStream(file);
 localFileOutputStream.write(newdex);
 localFileOutputStream.close();
 } catch (IOException localIOException) {
 throw new RuntimeException(localIOException);
 }
 
 //分析被加壳的apk文件
 ZipInputStream localZipInputStream = new ZipInputStream(
 new BufferedInputStream(new FileInputStream(file)));
 while (true) {
 ZipEntry localZipEntry = localZipInputStream.getNextEntry();//不了解这个是否也遍历子目录，看样子应该是遍历的
 if (localZipEntry == null) {
 localZipInputStream.close();
 break;
 }
 //取出被加壳apk用到的so文件，放到 libPath中（data/data/包名/payload_lib)
 String name = localZipEntry.getName();
 if (name.startsWith("lib/") && name.endsWith(".so")) {
 File storeFile = new File(libPath + "/"
 + name.substring(name.lastIndexOf('/')));
 storeFile.createNewFile();
 FileOutputStream fos = new FileOutputStream(storeFile);
 byte[] arrayOfByte = new byte[1024];
 while (true) {
 int i = localZipInputStream.read(arrayOfByte);
 if (i == -1)
 break;
 fos.write(arrayOfByte, 0, i);
 }
 fos.flush();
 fos.close();
 }
 localZipInputStream.closeEntry();
 }
 localZipInputStream.close();

 }

 /**
 * 从apk包里面获取dex文件内容（byte）
 * @return
 * @throws IOException
 */
 private byte[] readDexFileFromApk() throws IOException {
 ByteArrayOutputStream dexByteArrayOutputStream = new ByteArrayOutputStream();
 ZipInputStream localZipInputStream = new ZipInputStream(
 new BufferedInputStream(new FileInputStream(
 this.getApplicationInfo().sourceDir)));
 while (true) {
 ZipEntry localZipEntry = localZipInputStream.getNextEntry();
 if (localZipEntry == null) {
 localZipInputStream.close();
 break;
 }
 if (localZipEntry.getName().equals("classes.dex")) {
 byte[] arrayOfByte = new byte[1024];
 while (true) {
 int i = localZipInputStream.read(arrayOfByte);
 if (i == -1)
 break;
 dexByteArrayOutputStream.write(arrayOfByte, 0, i);
 }
 }
 localZipInputStream.closeEntry();
 }
 localZipInputStream.close();
 return dexByteArrayOutputStream.toByteArray();
 }

 // //直接返回数据，读者可以添加自己解密方法
 private byte[] decrypt(byte[] srcdata) {
 for(int i=0;i
- 从内存中dump DEX
- 构造完整调用链, 主动调用所有方法并dump CodeItem
- 合并 DEX, CodeItem

项目地址：[https://github.com/youlor/unpacker](http://imyhq.com/addons/cms/go/index.html?url=https%3A%2F%2Fgithub.com%2Fyoulor%2Funpacker)

在该地址中，有较多的流程及方法、注意问题等。

## 02 hook脱壳
通过利用frida框架对DexFile，OpenFile、dexFindClass等关键函数hook实现脱壳。

整体思路：

```
1.通过IDA打开libart.so文件，搜索关键函数
2.分析函数，编写hook脚本
3.使用frida附加进程进行dump，得到对应的dex
4.用jadx打开dex，尽情查看

```

## 03 特殊API调试脱壳
特殊API调试意思是指的通过Android系统提供的API方法，来获取Dex，在Android 7.0 及以下系统提供了getDex()及getBytes()这两个API,可以获得class对象，然后直接调用这两个API

![图片.png](https://cdn.nlark.com/yuque/0/2023/png/29674331/1681027418699-bc193cc3-2e75-4325-843c-a11b6a1a077f.png#averageHue=%23cc8573&clientId=u730e4549-c8cd-4&from=paste&height=302&id=u9bb4498d&name=%E5%9B%BE%E7%89%87.png&originHeight=453&originWidth=1027&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=98891&status=done&style=none&taskId=u544c54d8-aa86-4c5a-8615-1457b45d059&title=&width=684.6666666666666)

![图片.png](https://cdn.nlark.com/yuque/0/2023/png/29674331/1681027424983-dea9f3ba-38ce-4328-92f1-5a06fa517ab8.png#averageHue=%23fbfaf9&clientId=u730e4549-c8cd-4&from=paste&height=131&id=u41546ef5&name=%E5%9B%BE%E7%89%87.png&originHeight=196&originWidth=1013&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=26926&status=done&style=none&taskId=ufbc5b248-ecc3-4c92-931a-7679387c581&title=&width=675.3333333333334)

编写hook脚本，思路为：

```
1.使用frida枚举所有Classloader
2.确定正确的ClassLoader并获取目标类的class对象
3.通过class对象获取dex对象
4.通过dex对象获取内存字节流并保存

```

![图片.png](https://cdn.nlark.com/yuque/0/2023/png/29674331/1681027430634-cda117db-482e-4ca4-8777-d9265e0a6e8b.png#averageHue=%23252424&clientId=u730e4549-c8cd-4&from=paste&height=523&id=u999bb89a&name=%E5%9B%BE%E7%89%87.png&originHeight=785&originWidth=923&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=313411&status=done&style=none&taskId=u99cbe8b1-b223-4e18-8c63-6f069fcd7e0&title=&width=615.3333333333334)