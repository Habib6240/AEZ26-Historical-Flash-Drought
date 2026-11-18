# Notebooks

All notebooks were run by the author in Google Colab with Google Drive paths (`/content/drive/MyDrive/AEZ26_Final_Research_Data/...`). They are stored without outputs. Re-execution evidence below comes from a scratch environment (not Colab) on 2026-11-14.

| Notebook | Phase | Role | Re-execution evidence |
|---|---|---|---|
| `AEZ26_Phase2A_Daily_Backbone_AUTO_SAVE_Colab.ipynb` | 2A | Merges the CHIRPS, ERA5-Land and GLDAS daily extracts into the 9,497-day backbone | Not re-run: source extracts and the merge workflow are not available |
| `AEZ26_Phase2C_Flash_Drought_Detection_v3_FIRST_CROSSING_FIX_Colab.ipynb` | 2C | First-crossing detector; 39-event catalogue, three sensitivity catalogues, pentad table | Re-run from the stored backbone: pentad table (SHA-256 `44f76cbf…`) and catalogues byte-identical to the stored files |
| `AEZ26_Phase2D_Compound_Driver_Characterization_AUTO_SAVE_Colab.ipynb` | 2D | Event verification, seasonality, drivers | Re-run: the nine Phase 2D outputs matched the stored copies |
| `AEZ26_Phase2E_Native_Response_Alignment_AUTO_SAVE_Colab.ipynb` | 2E | Native-time alignment of MODIS, GRACE and JRC records to events | Not re-run: quality-control inputs not available |
| `AEZ26_Phase2F_Native_Response_Metrics_Lag_AUTO_SAVE_Colab_v2.ipynb` and `AEZ26_Phase2F_FINAL_Naming_QC_Patch_Colab.ipynb` | 2F | Response metrics and lags; the patch corrects naming of signed recovery offsets only | Not re-run: depends on the Phase 2E link tables |
| `AEZ26_Phase2G_Driver_Response_Statistical_Synthesis_AUTO_SAVE_Colab.ipynb` | 2G | 46 association tests with FDR control; fixed random seeds | Re-run: all nine stored outputs reproduced |
| `AEZ26_Phase7A_..._FINAL_DOCS_CORRECTED.ipynb` | 7A | Extended 1981–2025 robustness analysis; locks the SHA-256 of the legacy pentad table (file B) | Re-run with file B, the nine sanitised chunks and the 39-row catalogue: all QC gates passed; see `documentation/PHASE7A_INPUT_PROVENANCE.md` |

The Phase 7A notebook is the author's FINAL notebook with documentation corrected only: a provenance note, the lock comment and one markdown bullet, plus the placeholder for the private asset identifier. The lock hash, code and thresholds are unchanged (the syntax tree of every code cell equals the original's).

`superseded/` is a provenance collection, not part of the reproduction path: `AEZ26_Phase2C_Flash_Drought_Detection_Colab.ipynb` (first Phase 2C version) and the original Phase 7A FINAL notebook (identical to the author-run file except for the asset-identifier placeholder). Other superseded notebooks are not included.
