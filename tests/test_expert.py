"""
Unit Tests – Sistem Pakar Forward Chaining
Jalankan dengan: pytest tests/ -v
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from inference import forward_chaining
from knowledge_base import RULES, ALL_SYMPTOMS


# ─────────────────────────────────────────
# Edge Cases
# ─────────────────────────────────────────

class TestEdgeCases:
    def test_empty_symptoms_returns_empty(self):
        result = forward_chaining([])
        assert result == []

    def test_irrelevant_symptom_fires_nothing(self):
        # Gejala tunggal yang tidak memenuhi aturan manapun sendirian
        result = forward_chaining(["dekat_sayur_daun"])
        # dekat_sayur_daun tidak memenuhi semua kondisi satu rule manapun sendirian
        # (rule 6 perlu buah_berair_lendir juga)
        for r in result:
            rule = next((x for x in RULES if x["id"] == r["rule_id"]), None)
            assert rule is not None
            assert "dekat_sayur_daun" in rule["conditions"]

    def test_result_structure(self):
        result = forward_chaining(["sayur_layu", "tepi_kecoklatan", "suhu_kulkas_diatas_5"])
        for r in result:
            assert "rule_id" in r
            assert "diagnosis" in r
            assert "saran" in r
            assert isinstance(r["diagnosis"], str)
            assert isinstance(r["saran"], str)
            assert len(r["diagnosis"]) > 0
            assert len(r["saran"]) > 0


# ─────────────────────────────────────────
# Specific Rule Tests
# ─────────────────────────────────────────

class TestSpecificRules:
    def _get_rule_ids(self, symptoms):
        return {r["rule_id"] for r in forward_chaining(symptoms)}

    def test_rule_1_sayur_suhu_tinggi(self):
        ids = self._get_rule_ids(["sayur_layu", "tepi_kecoklatan", "suhu_kulkas_diatas_5"])
        assert 1 in ids

    def test_rule_2_freezer_burn(self):
        ids = self._get_rule_ids(["daging_pucat", "kristal_es"])
        assert 2 in ids

    def test_rule_3_skincare_vit_c(self):
        ids = self._get_rule_ids(["skincare_vit_c_berubah_warna"])
        assert 3 in ids

    def test_rule_4_herbal_gumpal_apek(self):
        ids = self._get_rule_ids(["herbal_gumpal", "bau_apek"])
        assert 4 in ids

    def test_rule_5_susu_basi_sering_dibuka(self):
        ids = self._get_rule_ids(["susu_basi_sebelum_exp", "kulkas_sering_dibuka"])
        assert 5 in ids

    def test_rule_6_buah_dekat_sayur(self):
        ids = self._get_rule_ids(["buah_berair_lendir", "dekat_sayur_daun"])
        assert 6 in ids

    def test_rule_7_freezer_bau_amis(self):
        ids = self._get_rule_ids(["freezer_bau_amis"])
        assert 7 in ids

    def test_rule_8_skincare_pecah(self):
        ids = self._get_rule_ids(["skincare_pecah"])
        assert 8 in ids

    def test_rule_9_sayur_layu_kulkas_penuh(self):
        ids = self._get_rule_ids(["sayur_layu_cepat", "kulkas_penuh"])
        assert 9 in ids

    def test_rule_10_daging_cair_merah(self):
        ids = self._get_rule_ids(["daging_cair_merah"])
        assert 10 in ids

    def test_rule_11_sayur_layu_kulkas_penuh(self):
        ids = self._get_rule_ids(["sayur_layu", "kulkas_penuh"])
        assert 11 in ids

    def test_rule_12_kristal_es_sering_dibuka(self):
        ids = self._get_rule_ids(["kristal_es", "kulkas_sering_dibuka"])
        assert 12 in ids

    def test_rule_13_susu_suhu_tinggi(self):
        ids = self._get_rule_ids(["susu_basi_sebelum_exp", "suhu_kulkas_diatas_5"])
        assert 13 in ids

    def test_rule_14_herbal_gumpal_alone(self):
        ids = self._get_rule_ids(["herbal_gumpal"])
        assert 14 in ids

    def test_rule_15_buah_berair_alone(self):
        ids = self._get_rule_ids(["buah_berair_lendir"])
        assert 15 in ids

    def test_rule_16_daging_pucat_suhu_tinggi(self):
        ids = self._get_rule_ids(["daging_pucat", "suhu_kulkas_diatas_5"])
        assert 16 in ids


# ─────────────────────────────────────────
# Multiple Rules Fired
# ─────────────────────────────────────────

class TestMultipleRules:
    def test_multiple_symptoms_fire_multiple_rules(self):
        symptoms = [
            "sayur_layu", "tepi_kecoklatan", "suhu_kulkas_diatas_5",
            "daging_pucat", "kristal_es",
        ]
        result = forward_chaining(symptoms)
        rule_ids = {r["rule_id"] for r in result}
        assert 1 in rule_ids
        assert 2 in rule_ids

    def test_no_duplicate_rule_fires(self):
        symptoms = [
            "sayur_layu", "tepi_kecoklatan", "suhu_kulkas_diatas_5",
        ]
        result = forward_chaining(symptoms)
        ids = [r["rule_id"] for r in result]
        assert len(ids) == len(set(ids))

    def test_all_symptoms_fires_multiple(self):
        result = forward_chaining(ALL_SYMPTOMS)
        assert len(result) >= 10, f"Expected >=10 rules fired, got {len(result)}"


# ─────────────────────────────────────────
# Negative Tests (should NOT fire)
# ─────────────────────────────────────────

class TestNegativeRules:
    def _get_rule_ids(self, symptoms):
        return {r["rule_id"] for r in forward_chaining(symptoms)}

    def test_rule_1_needs_all_3_conditions(self):
        # Hanya 2 kondisi → rule 1 tidak boleh terpicu
        ids = self._get_rule_ids(["sayur_layu", "tepi_kecoklatan"])
        assert 1 not in ids

    def test_rule_2_needs_both_conditions(self):
        ids = self._get_rule_ids(["daging_pucat"])
        assert 2 not in ids

    def test_rule_6_needs_both_conditions(self):
        ids = self._get_rule_ids(["dekat_sayur_daun"])
        assert 6 not in ids

    def test_unrelated_symptoms_dont_fire_freezer_rules(self):
        ids = self._get_rule_ids(["skincare_vit_c_berubah_warna"])
        # Rule 7 (freezer_bau_amis) tidak boleh terpicu
        assert 7 not in ids


# ─────────────────────────────────────────
# Knowledge Base Integrity
# ─────────────────────────────────────────

class TestKnowledgeBase:
    def test_all_rules_have_required_keys(self):
        for rule in RULES:
            assert "id" in rule
            assert "conditions" in rule
            assert "conclusion" in rule
            assert "diagnosis" in rule["conclusion"]
            assert "saran" in rule["conclusion"]

    def test_rule_ids_are_unique(self):
        ids = [r["id"] for r in RULES]
        assert len(ids) == len(set(ids))

    def test_all_rule_conditions_in_symptom_list(self):
        symptom_set = set(ALL_SYMPTOMS)
        for rule in RULES:
            for cond in rule["conditions"]:
                assert cond in symptom_set, f"Condition '{cond}' in rule {rule['id']} not in ALL_SYMPTOMS"

    def test_minimum_rules_count(self):
        assert len(RULES) >= 12

    def test_all_symptoms_non_empty(self):
        assert len(ALL_SYMPTOMS) > 0
        for s in ALL_SYMPTOMS:
            assert isinstance(s, str) and len(s) > 0
