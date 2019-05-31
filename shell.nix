{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell {
    name = "Python";
    buildInputs = [
        (python37.withPackages(ps: with ps; [
            autopep8
            flake8
            mypy
            numpy
            pytest
            pytz
            slackclient
            statsmodels
        ]))
    ];
    shellHook = ''
        . .shellhook
    '';
}
