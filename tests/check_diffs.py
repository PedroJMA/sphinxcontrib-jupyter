"""
Check diffs for each test file

Diff Configuration
------------------
Currently this is setup to ignore metadata as the extension will generate
a minimal notebook. So opening a notebook and saving will add metadata
that will cause the diff checker to fail.

"""

import nbformat
import glob
import os
from nbdime.diffing.notebooks import diff_notebooks, set_notebook_diff_targets

NB_VERSION = 4
GENERATED_IPYNB_FILES = glob.glob("_build/jupyter/*.ipynb")
REFERENCE_IPYNB_FILES = [os.path.basename(
    fl) for fl in glob.glob("ipynb/*.ipynb")]
SKIP = ["index.ipynb"]

#-Diff Configuration-#
set_notebook_diff_targets(metadata=False)

for fl in GENERATED_IPYNB_FILES:
    flname = fl.split("/")[-1]
    if flname in SKIP:
        continue
    print("Testing {} ...".format(fl))
    if flname not in REFERENCE_IPYNB_FILES:
        print("[FAIL] Notebook {} has no matching test case in ipynb/".format(flname))
        exit(1)
    nb1 = nbformat.read(fl, NB_VERSION)
    nb2 = nbformat.read(os.path.join("ipynb", flname), NB_VERSION)
    diff = diff_notebooks(nb1, nb2)
    if len(diff) != 0:
        print("[FAIL] {} and {} are different:".format(
            fl, os.path.join("ipynb", flname)))
        print(diff)
        exit(1)

exit(0)
