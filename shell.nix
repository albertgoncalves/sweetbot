{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell {
    name = "Python";
    buildInputs = [
        (python36.withPackages(ps: with ps; [
            slackclient
            statsmodels
            numpy
            pytz
            pytest
            mypy
            flake8
        ]))
        coreutils
    ];
    shellHook = ''
        . .alias
        if [ ! -d imgs/ ]; then
            mkdir imgs/
        fi
    '';
}
