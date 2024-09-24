{ stdenv
, fetchFromGitHub
, python3Packages
, makeWrapper
, lib
, ... }:

let
  python = python3Packages.python;
  pyperclip = python3Packages.pyperclip;
  tkinter = python3Packages.tkinter;
  sitePackagesPath = builtins.concatStringsSep ":" [
    "${pyperclip}/${python.libPrefix}/site-packages"
    "${tkinter}/${python.libPrefix}/site-packages"
  ];
in

stdenv.mkDerivation rec {
  pname = "colorizz";
  version = "1.0";

  src = ./.;

  nativeBuildInputs = [ makeWrapper ];

  propagatedBuildInputs = [ pyperclip tkinter ];

  installPhase = ''
    mkdir -p "$out/bin"
    cp "${src}/colorizz.py" "$out/bin/colorizz"
    chmod +x "$out/bin/colorizz"

    # Add shebang line
    sed -i "1i #!${python}/bin/python" "$out/bin/colorizz"

    # Wrap the script to set PYTHONPATH with multiple paths
    wrapProgram "$out/bin/colorizz" \
      --prefix PYTHONPATH : "${sitePackagesPath}"
  '';

  meta = with lib; {
    description = "Colorizz script";
    homepage = "https://github.com/duncanturk/colorizz";
    license = licenses.mit;  # Update if necessary
    maintainers = [];
  };
}
