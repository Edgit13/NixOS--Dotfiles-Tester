{ config, lib, pkgs, ... }:

{
  imports = [ ./hardware-configuration.nix ];

  # Дозволяємо платне ПЗ (vscode тощо)
  nixpkgs.config.allowUnfree = true;

  # Завантажувач та мережа
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  networking.hostName = "EduardPC";
  networking.networkmanager.enable = true;
  time.timeZone = "Europe/Kyiv";

  # Bluetooth
  hardware.bluetooth.enable = true;
  hardware.bluetooth.powerOnBoot = true;
  services.blueman.enable = true;

  # Віконний менеджер Qtile
  services.xserver = {
    enable = true;
    windowManager.qtile.enable = true;
    displayManager.sessionCommands = ''
      xwallpaper --zoom ~/walls/wall1.jpg &
      xset r rate 200 35 &
    '';
    xkb.layout = "us,ua";
    xkb.options = "grp:win_space_toggle";
  };

  # Звук (Pipewire)
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    wireplumber.enable = true;
  };

  # Твій користувач
  users.users.eduard = {
    isNormalUser = true;
    extraGroups = [ "wheel" "docker" "networkmanager" "audio" "video" ];
  };

  # Сервіси
  virtualisation.docker.enable = true;
  programs.firefox.enable = true;

  # ОСЬ ТУТ ВСІ ТВОЇ ПРОГРАМИ
  environment.systemPackages = with pkgs; [
    # Термінал та редактори
    alacritty
    vim
    neovim
    vscode
    gedit
    
    # Файлові менеджери та утиліти
    nautilus
    yazi
    git
    wget
    btop
    tree
    xclip
    
    # Графіка та Qtile
    xwallpaper
    nitrogen
    picom
    rofi
    networkmanagerapplet
    blueman
    
    # Звук (пакети, які ми додавали)
    pamixer
    pavucontrol
    pulseaudio
    
    # Docker
    docker
  ];

  system.stateVersion = "25.11"; 
}
