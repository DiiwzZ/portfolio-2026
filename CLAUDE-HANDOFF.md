# Portfolio — Handoff Guide for Claude Code

## โปรเจกต์นี้คืออะไร
Portfolio ส่วนตัวของ **Vuttipat Prapai (Dew)** สำหรับสมัครงาน 2 ตำแหน่ง:
- **AI Specialist** (เน้นหลัก)
- **Graphic Designer** (รอง)

Deploy ที่: `https://diiwzz.github.io/portfolio/`
Repo: `DiiwzZ/portfolio` (branch: `master`)

---

## โครงสร้างไฟล์
```
index.html      ← ทุกอย่างอยู่ในไฟล์เดียว (HTML + CSS + JS inline)
images/         ← รูปผลงานทั้งหมด
```

**สำคัญ:** repo เดิมมี `styles.css` และ `script.js` — **ลบทิ้งได้** เพราะรวมเข้า `index.html` แล้ว

---

## ลำดับ Section
1. **Hero** — ชื่อ + typing animation (roles หมุน)
2. **About** — copy + skills 3 กลุ่ม (AI & LLMs / Creative Tools / Development)
3. **Experience** — งานจริง (สำคัญที่สุด อยู่บน)
4. **Projects** — งานเรียน (Academic & Design Projects)
5. **Contact**

---

## Design System

### สี (CSS variables ใน `:root`)
```css
--bg: #080808          /* พื้นหลังหลัก */
--bg1: #0f0f0f         /* card */
--bg2: #161616         /* nested card */
--border: #242424
--text: #e8e8e8
--text-dim: #888
--text-faint: #444
--accent: oklch(72% 0.14 195)   /* teal — ใช้เน้น AI */
--gold: #e8a833                 /* ใช้กับ featured badge */
```

### กฎการใช้สี
- **accent (teal)** = ทุกอย่างที่เกี่ยวกับ AI (tag, badge, border ของ AI card)
- **gold** = featured project badge เท่านั้น
- ห้ามเพิ่มสีใหม่ ถ้าจำเป็นให้ใช้ `oklch()` ให้กลมกลืนกับ palette เดิม

### Typography
System font stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI'...`) — **ห้ามเปลี่ยนเป็น Google Font**

---

## สิ่งที่ยังต้องทำ (TODO)

### 1. Work Samples — ยังเป็น placeholder
อยู่ใน Experience → card แรก (AI-Driven Content Workflow) → section "Featured Work Samples"

มี 3 ช่องรอข้อมูล:

| ช่อง | ต้องการ |
|---|---|
| Article Graphic | รูป + ชื่อบทความ + link + จำนวน reads |
| Facebook Infographic | รูป + ชื่อโพส + link + likes + shares |
| Short Video | thumbnail + ชื่อคลิป + link FB Reel + link TikTok + ยอดวิว 2 platform |

**วิธีแก้:** หา `<!-- 1. Article Graphic -->` ใน `index.html` แล้วแทนที่:
- `<div style="text-align:center;color:var(--text-faint);">...</div>` (placeholder icon) → `<img src="images/...">`
- `ชื่อบทความ / Article Title` → ชื่อจริง
- `— reads` → ตัวเลขจริง
- `href="#"` → URL จริง

### 2. วิดีโอ After Effects
`Product_Banner.mp4` ใหญ่เกิน push ขึ้น GitHub — ตอนนี้แสดงเป็น "Available upon request"
ถ้าอยากให้ดูได้ → อัพ YouTube แล้วเปลี่ยนเป็น embed หรือ link

### 3. Resume/CV
ยังไม่มีปุ่ม download — ถ้ามี PDF ให้เพิ่มใน Hero actions หรือ Contact section

---

## กฎการแก้ไข

### ต้องทำ
- แก้เฉพาะที่ขอ อย่าไป redesign ส่วนอื่น
- ใช้ CSS variables ที่มีอยู่ ไม่ hardcode สี
- เขียน HTML แบบ compact (ไม่ต้อง indent เยอะ)
- Layout ใช้ flex/grid + `gap` เสมอ

### ห้ามทำ
- ห้ามเพิ่ม content ที่ไม่มีจริง (เคยลบ "Staff Training" ออกเพราะยังไม่มีประสบการณ์)
- ห้ามเพิ่ม emoji นอกจากที่มีอยู่แล้วใน exp-icon
- ห้ามเปลี่ยน font
- ห้าม oversell — เขียนตามที่ทำจริง

---

## Context สำคัญ

### ทำไม Experience อยู่ก่อน Projects
เพราะงาน internship จริงน่าสนใจกว่างานเรียน — ให้คนอ่านเจอก่อน

### ทำไม Nano Banana อยู่ใน Experience ไม่ใช่ Projects
เพราะสร้างขึ้นระหว่างฝึกงานเพื่อแก้ปัญหาจริง (ทำกราฟิกทีละรูปช้า) — เป็นหลักฐาน "Workflow Optimization" ตรง JD

### JD ที่ portfolio ต้อง cover
**AI Specialist:**
- AI Implementation ✅ (Nano Banana)
- Workflow Optimization ✅ (batch generation)
- Prompt Engineering ✅
- Data Analysis ⚠️ (ยังไม่มีผลงาน)
- AI Ethics & QC ✅ (ใน What I Learned)
- Python bonus ✅ (Flask)

**Graphic Design:**
- Illustrator/Photoshop ✅
- ป้ายโฆษณา/print ✅ (Maginta)
- SketchUp 3D ❌ (ไม่มี)

---

## Deploy
```bash
git add .
git commit -m "update portfolio"
git push origin master
```
GitHub Pages จะอัพเดทเองภายใน 1-2 นาที
