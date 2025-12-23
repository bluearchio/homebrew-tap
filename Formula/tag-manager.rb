class TagManager < Formula
  desc "AWS Tag Manager CLI - FinOps, compliance, and cost optimization tool"
  homepage "https://bluearch.io"
  version "0.0.0"
  license :cannot_represent

  depends_on arch: :arm64

  url "https://dist.bluearch.io/tag-manager/latest/tag-manager_macos_arm64"
  sha256 "PLACEHOLDER_SHA256"

  def install
    bin.install "tag-manager_macos_arm64" => "tag-manager"
  end

  test do
    system "#{bin}/tag-manager", "--version"
  end
end
