# Signing Audit

Snapshot: Soft-Imóveis Desktop V0.2 Development Build

Distribution audited:

```text
dist/SoftImoveis
```

## Summary

- Total EXE/DLL/PYD: 67
- Valid: 53
- NotSigned: 14

## Details

| arquivo | tipo | assinatura | publisher | status | observação |
|---|---|---|---|---|---|
| SoftImoveis.exe | EXE | NotSigned |  | NotSigned | Artefato próprio; assinar em release. |
| _internal\_bz2.pyd | PYD | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\_decimal.pyd | PYD | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\_hashlib.pyd | PYD | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\_lzma.pyd | PYD | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\_queue.pyd | PYD | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\_socket.pyd | PYD | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\_ssl.pyd | PYD | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\libcrypto-3-x64.dll | DLL | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\libssl-3-x64.dll | DLL | NotSigned |  | NotSigned | Binário Python/OpenSSL empacotado; pendente de validação durante signed release. |
| _internal\python3.dll | DLL | NotSigned |  | NotSigned | Binário Python empacotado; pendente de validação durante signed release. |
| _internal\python312.dll | DLL | NotSigned |  | NotSigned | Binário Python empacotado; pendente de validação durante signed release. |
| _internal\select.pyd | PYD | NotSigned |  | NotSigned | Binário Python empacotado; pendente de validação durante signed release. |
| _internal\unicodedata.pyd | PYD | NotSigned |  | NotSigned | Binário Python empacotado; pendente de validação durante signed release. |
| PySide6 / Qt DLLs e PYDs | DLL/PYD | Valid | The Qt Company Oy | Valid | Assinatura válida do fornecedor. |
| VCRUNTIME140*.dll | DLL | Valid | Microsoft Windows Software Compatibility Publisher | Valid | Assinatura válida do fornecedor. |

## Notes

- Este documento é auditoria, não ação de assinatura.
- `SoftImoveis.exe` é o artefato próprio do projeto e deve ser assinado no pipeline de release.
- Binários de terceiros não devem ser modificados automaticamente sem avaliação da origem.
