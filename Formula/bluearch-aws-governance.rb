class BluearchAwsGovernance < Formula
  desc "AWS Governance Hub with bundled misconfiguration catalog"
  homepage "https://github.com/bluearchio/bluearch-aws-governance"
  url "https://dist.bluearch.io/releases/bluearch-aws-governance/v0.2.3/cloud-governance-macos-arm64.zip"
  version "v0.2.3"
  sha256 "9ac6a80449f0b32a31e0b0557f3116afaa5b85b1280d4fa048064a2b507adb73"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "cloud-governance"
    alias_path = bin/"bluearch-aws-governance"
    alias_path.write <<~SH
      #!/bin/sh
      exec "#{bin}/cloud-governance" "$@"
    SH
    alias_path.chmod 0755
  end

  def caveats
    <<~EOS
      bluearch-aws-governance has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-governance --help
        cloud-governance --help

      Load the bundled catalog:
        bluearch-aws-governance catalog load
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-governance", "--version"
    system "#{bin}/cloud-governance", "--version"
  end
end
