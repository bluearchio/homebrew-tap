class BluearchAwsGovernance < Formula
  desc "AWS Governance Hub with bundled misconfiguration catalog"
  homepage "https://github.com/bluearchio/bluearch-aws-governance"
  url "https://dist.bluearch.io/releases/bluearch-aws-governance/v0.2.3/bluearch-aws-governance-macos-arm64.zip"
  version "v0.2.3"
  sha256 "9b1356098157682c724f1f18bda414337fad688a6d0ab0c4574ac0fecb16b653"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "bluearch-aws-governance"
  end

  def caveats
    <<~EOS
      bluearch-aws-governance has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-governance --help

      Load the bundled catalog:
        bluearch-aws-governance catalog load
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-governance", "--version"
  end
end
