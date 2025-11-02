# 🧾 LoAI QR Verification Block Template

This block creates a scannable proof of authenticity for any verified LoAI document, blueprint, or compliance file.  
It embeds a QR payload linking to the associated checksum verification file within the LoAI Global Registry.

---

## 🔗 Example Block (Markdown Embed)

| Verification Seal | Description |
|:--:|:--|
| ![LoAI Verified QR](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://suscarver75-ui.github.io/global-ai-registry/spec/loai-medical-ai-v2.0-checksum.md) | **LoAI Verified Ledger — Medical-AI v2.0**<br>Scan to verify checksum authenticity and registry status.<br><br>**Registry Anchor:** LoAI-2024-0414-001<br>**DID:** did:web:suscarver75-ui.github.io<br>**Checksum Status:** 🟢 Pending → ✅ Verified<br>**Algorithm:** SHA-512 |

---

## 🧩 Developer Notes
- The QR automatically links to the checksum file for that document.  
- Replace the URL in `data=` with the path to the checksum `.md` file for future versions.  
- Use this block in any README, registry, or spec page.  
- Ideal placement: bottom-right section or under “Legal & Protection Layer.”  
- For added security, embed your LoAI Seal image next to the QR.

---

### 📘 Example Footer (for embedding)
```markdown
> ![LoAI Seal](https://suscarver75-ui.github.io/global-ai-registry/assets/loai-verified-seal.png)
> 
> Scan QR or visit [Checksum Verification → LoAI-MEDICAL-AI-v2.0](/spec/loai-medical-ai-v2.0-checksum.md)

---

## ✅ After Upload
1. Add this file to your `/templates/` folder.  
2. Then link it in your main `README.md`:
   ```markdown
   - [QR Verification Block Template](/templates/qr-verification-block.md)
