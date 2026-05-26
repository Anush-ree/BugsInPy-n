# BugsInPy Duplicate Bug Clusters — Test Overlap

Stricter duplicate detection using shared **failing tests** (via `run_test.sh` / `test.sh`).

**Total clusters found: 14**

---

## keras

| Bugs               | Shared Failing Test                                       |
| ------------------ | --------------------------------------------------------- |
| keras-42, keras-13 | `tests/keras/engine/test_training.py::test_model_methods` |

---

## thefuck

| Bugs                  | Shared Failing Test                                  |
| --------------------- | ---------------------------------------------------- |
| thefuck-9, thefuck-11 | `tests/rules/test_git_push.py::test_get_new_command` |

---

## tqdm

| Bugs           | Shared Failing Test                           |
| -------------- | --------------------------------------------- |
| tqdm-8, tqdm-2 | `tqdm/tests/tests_tqdm.py::test_format_meter` |
| tqdm-3, tqdm-5 | `tqdm/tests/tests_tqdm.py::test_bool`         |

---

## matplotlib

| Bugs                         | Shared Failing Test                                          |
| ---------------------------- | ------------------------------------------------------------ |
| matplotlib-18, matplotlib-19 | `lib/matplotlib/tests/test_axes.py::test_polar_no_data`      |
| matplotlib-16, matplotlib-17 | `lib/matplotlib/tests/test_colorbar.py::test_colorbar_int`   |
| matplotlib-26, matplotlib-24 | `lib/matplotlib/tests/test_axes.py::test_set_ticks_inverted` |

---

## youtube-dl

| Bugs                                                      | Shared Failing Test                                                     |
| --------------------------------------------------------- | ----------------------------------------------------------------------- |
| youtube-dl-35, youtube-dl-29, youtube-dl-41               | `test.test_utils.TestUtil.test_unified_dates`                           |
| youtube-dl-27, youtube-dl-6                               | `test.test_utils.TestUtil.test_parse_dfxp_time_expr`                    |
| youtube-dl-9, youtube-dl-8                                | `test.test_YoutubeDL.TestFormatSelection.test_youtube_format_selection` |
| youtube-dl-7, youtube-dl-10, youtube-dl-26, youtube-dl-25 | `test.test_utils.TestUtil.test_js_to_json_realworld`                    |
| youtube-dl-28, youtube-dl-3                               | `test.test_utils.TestUtil.test_unescape_html`                           |
| youtube-dl-21, youtube-dl-13                              | `test.test_utils.TestUtil.test_urljoin`                                 |
| youtube-dl-24, youtube-dl-22                              | `test.test_YoutubeDL.TestYoutubeDL.test_match_filter`                   |

---

## Summary

| Project    | Clusters | Notes                                                   |
| ---------- | -------- | ------------------------------------------------------- |
| keras      | 1        | —                                                       |
| thefuck    | 1        | Also flagged by file-overlap                            |
| tqdm       | 2        | Also flagged by file-overlap                            |
| matplotlib | 3        | All 3 also flagged by file-overlap — highest confidence |
| youtube-dl | 7        | Dominates; all in `test_utils` or `test_YoutubeDL`      |

> **Highest-confidence duplicates** (appear in both file-overlap and test-overlap):
> `matplotlib-16/17`, `matplotlib-26/24`, `thefuck-9/11`, `tqdm-3/5`, `tqdm-8/2`
