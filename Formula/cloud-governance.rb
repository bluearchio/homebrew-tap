class CloudGovernance < Formula
  desc "BlueArch Governance Hub"
  homepage "https://bluearch.io"
  url "https://dist.bluearch.io/cloud-governance/v0.2.2/cloud-governance_macos_arm64"
  version "v0.2.2"
  sha256 "79cf0c2c0a7ea3740f6b52f80cec39d8a7c30d7ae057e3472ee80e7232e54a01"
  license :cannot_represent

  depends_on arch: :arm64
  depends_on "bluearch-core"

  def install
    bin.install "cloud-governance_macos_arm64" => "cloud-governance"
  end

  def caveats
    <<~EOS
      Governance Hub has been installed.

      Start BlueArch Core to launch installed dashboards:
        bluearch-core start --daemon
    EOS
  end

  test do
    system "#{bin}/cloud-governance", "--version"
  end
end
