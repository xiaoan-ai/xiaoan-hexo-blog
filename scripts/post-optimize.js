const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const POSTS_DIR = path.join(__dirname, '../source/_posts');
const ALLOWED_CATEGORIES = ['日记', '散文', '笔记', '研究'];

// 优化单个文章
function optimizePost(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const { data, content: body } = matter(content);
    
    // 1. 修复分类
    if (!data.categories || !Array.isArray(data.categories)) {
        data.categories = [];
    }
    // 过滤无效分类，只保留允许的
    data.categories = data.categories.filter(cat => ALLOWED_CATEGORIES.includes(cat));
    // 如果没有有效分类，自动识别
    if (data.categories.length === 0) {
        const title = (data.title || '').toLowerCase();
        const bodyLower = body.toLowerCase();
        if (title.includes('日记') || bodyLower.includes('今日') || bodyLower.includes('每日') || bodyLower.includes('成长记录')) {
            data.categories.push('日记');
        } else if (title.includes('研究') || bodyLower.includes('系统设计') || bodyLower.includes('架构') || bodyLower.includes('分析')) {
            data.categories.push('研究');
        } else if (title.includes('笔记') || bodyLower.includes('学习') || bodyLower.includes('知识点')) {
            data.categories.push('笔记');
        } else {
            data.categories.push('散文');
        }
    }
    
    // 2. 标题：不在这里做“去标点/清洗”处理。
    // 之前的实现会把“｜”“：”“引号”等标点全部删掉，导致标题风格被破坏。
    // 如果需要修复乱码，应在专用脚本中做一次性处理，而不是在 Hexo 每次运行时自动改标题。
    data.title = (data.title || path.basename(filePath, '.md')).trim();
    
    // 3. 标准化markdown格式
    let optimizedBody = body
        // 标题层级：# 后面加空格
        .replace(/^(#+)([^#\s])/gm, '$1 $2')
        // 段落间距：两个换行分隔段落
        .replace(/\n{3,}/g, '\n\n')
        // 代码块：``` 后面加语言标注（如果没有）
        .replace(/```\n/g, '```text\n')
        // 引用块：> 后面加空格
        .replace(/^>([^>\s])/gm, '> $1');
    
    // 4. 生成新文件名：日期-标题.md
    const dateStr = data.date ? new Date(data.date).toISOString().split('T')[0] : path.basename(filePath).match(/^\d{4}-\d{2}-\d{2}/)?.[0] || '';
    const slug = data.title
        .replace(/\s+/g, '-')
        .replace(/[^\u4e00-\u9fa5a-zA-Z0-9\-]/g, '')
        .toLowerCase();
    const newFileName = `${dateStr}-${slug}.md`.replace(/^-+/, '');
    
    // 生成优化后的内容
    const optimizedContent = matter.stringify(optimizedBody, data, {
        language: 'yaml',
        lineWidth: -1
    });
    
    return {
        oldPath: filePath,
        newFileName,
        content: optimizedContent,
        changes: {
            title: data.title,
            category: data.categories[0],
            newFileName
        }
    };
}

// 批量优化所有文章
function optimizeAllPosts() {
    const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
    const results = [];
    
    for (const file of files) {
        const filePath = path.join(POSTS_DIR, file);
        try {
            const result = optimizePost(filePath);
            // 写入新文件
            fs.writeFileSync(path.join(POSTS_DIR, result.newFileName), result.content, 'utf8');
            // 删除旧文件
            if (path.basename(filePath) !== result.newFileName) {
                fs.unlinkSync(filePath);
            }
            results.push({
                oldName: file,
                newName: result.newFileName,
                ...result.changes
            });
            console.log(`✅ 优化完成: ${file} → ${result.newFileName}`);
        } catch (e) {
            console.error(`❌ 优化失败: ${file}`, e.message);
        }
    }
    
    // 生成优化报告
    const report = `# 博客文章优化报告
## 优化时间: ${new Date().toLocaleString('zh-CN')}
## 优化文章数: ${results.length} 篇
## 优化详情:
| 原文件名 | 新文件名 | 新标题 | 分类 |
| --- | --- | --- | --- |
${results.map(r => `| ${r.oldName} | ${r.newName} | ${r.title} | ${r.category} |`).join('\n')}
`;
    
    fs.writeFileSync(path.join(__dirname, '../optimize-report.md'), report, 'utf8');
    console.log('\n📝 优化报告已生成: optimize-report.md');
    return results;
}

// 校验所有文章是否符合规范
function validatePosts() {
    const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
    const errors = [];
    
    for (const file of files) {
        const filePath = path.join(POSTS_DIR, file);
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const { data } = matter(content);
            
            // 校验分类
            if (!data.categories || data.categories.length === 0) {
                errors.push(`${file}: 缺少分类`);
            } else if (!ALLOWED_CATEGORIES.includes(data.categories[0])) {
                errors.push(`${file}: 无效分类 ${data.categories[0]}，允许的分类: ${ALLOWED_CATEGORIES.join(',')}`);
            }
            
            // 校验标题
            if (!data.title || data.title.trim().length === 0) {
                errors.push(`${file}: 缺少标题`);
            }
            
            // 校验文件名格式
            if (!/^\d{4}-\d{2}-\d{2}-.+\.md$/.test(file)) {
                errors.push(`${file}: 文件名格式错误，应为 日期-标题.md`);
            }
            
        } catch (e) {
            errors.push(`${file}: 解析失败: ${e.message}`);
        }
    }
    
    if (errors.length === 0) {
        console.log('✅ 所有文章校验通过');
        return true;
    } else {
        console.error('❌ 校验失败，存在以下问题:');
        errors.forEach(e => console.error(`  - ${e}`));
        return false;
    }
}

// 运行
// 注意：Hexo 会自动加载 scripts/ 目录下的 .js 文件。
// 为避免“每次 hexo clean/generate/deploy 都自动改文章标题/文件名”，这里默认不自动执行。
// 如需手动优化：
//   POST_OPTIMIZE_RUN=1 node scripts/post-optimize.js
// 或仅校验：
//   node scripts/post-optimize.js --validate
if (process.argv.includes('--validate')) {
    process.exit(validatePosts() ? 0 : 1);
}

if (process.env.POST_OPTIMIZE_RUN === '1') {
    optimizeAllPosts();
    process.exit(validatePosts() ? 0 : 1);
}
