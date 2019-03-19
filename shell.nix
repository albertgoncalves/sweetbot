{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell {
    name = "Python";
    buildInputs = [
        (python36.withPackages(ps: with ps; [
            flake8
            pytest
            mypy
            numpy
            pytz
            slackclient
            statsmodels
        ]))
    ];
    shellHook = ''
        . .alias
    '';
}
